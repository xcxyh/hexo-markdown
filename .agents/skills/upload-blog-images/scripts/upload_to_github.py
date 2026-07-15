#!/usr/bin/env python3
"""Upload blog images to a GitHub branch and print immutable CDN URLs."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath


ALLOWED_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".gif",
    ".svg",
    ".avif",
    ".heic",
}
RASTER_TO_WEBP = {".png", ".jpg", ".jpeg"}


@dataclass(frozen=True)
class Asset:
    source: Path
    prepared: Path
    target_name: str
    digest: str


def run(command: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"Command failed: {' '.join(command)}\n{details}")
    return result.stdout.strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or "image"


def validate_source(path_text: str) -> Path:
    path = Path(path_text).expanduser().resolve()
    if not path.is_file():
        raise ValueError(f"Image does not exist: {path}")
    if path.stat().st_size == 0:
        raise ValueError(f"Image is empty: {path}")
    if path.suffix.lower() not in ALLOWED_SUFFIXES:
        allowed = ", ".join(sorted(ALLOWED_SUFFIXES))
        raise ValueError(f"Unsupported image type for {path}; expected one of: {allowed}")
    return path


def optimize_to_webp(source: Path, output: Path, quality: int) -> Path:
    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise RuntimeError(
            "--optimize-raster requires Pillow. Use a Python runtime with Pillow "
            "or prepare WebP files separately."
        ) from exc

    with Image.open(source) as image:
        image = ImageOps.exif_transpose(image)
        if image.mode not in {"RGB", "RGBA"}:
            image = image.convert("RGBA" if "transparency" in image.info else "RGB")
        image.save(output, format="WEBP", quality=quality, method=6)
    return output


def prepare_assets(
    file_names: list[str],
    workspace: Path,
    prefix: str,
    optimize_raster: bool,
    quality: int,
) -> list[Asset]:
    assets: list[Asset] = []
    seen_targets: set[str] = set()
    safe_prefix = slugify(prefix)

    for index, file_name in enumerate(file_names):
        source = validate_source(file_name)
        prepared = source
        if optimize_raster and source.suffix.lower() in RASTER_TO_WEBP:
            prepared = workspace / f"{index}-{slugify(source.stem)}.webp"
            optimize_to_webp(source, prepared, quality)

        digest = sha256(prepared)
        target_name = (
            f"{safe_prefix}-{slugify(source.stem)}-{digest[:8]}"
            f"{prepared.suffix.lower()}"
        )
        if target_name in seen_targets:
            continue
        seen_targets.add(target_name)
        assets.append(Asset(source, prepared, target_name, digest))

    return assets


def parse_repo(repo: str) -> tuple[str, str, str]:
    cleaned = repo.strip().removesuffix(".git")
    if cleaned.startswith("git@github.com:"):
        slug = cleaned.split(":", 1)[1]
        remote = f"{cleaned}.git"
    elif cleaned.startswith("https://github.com/"):
        slug = cleaned.removeprefix("https://github.com/")
        remote = f"https://github.com/{slug}.git"
    else:
        slug = cleaned.strip("/")
        remote = f"git@github.com:{slug}.git"
    parts = slug.split("/")
    if len(parts) != 2 or not all(parts):
        raise ValueError("--repo must be owner/repository or a GitHub repository URL")
    return parts[0], parts[1], remote


def validate_target_dir(value: str) -> str:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise ValueError("--target-dir must be a relative path inside the repository")
    return path.as_posix().strip("/")


def build_url(
    owner: str,
    repository: str,
    branch: str,
    commit: str,
    target_dir: str,
    target_name: str,
    url_mode: str,
) -> str:
    path = PurePosixPath(target_dir, target_name).as_posix()
    if url_mode == "raw-branch":
        return f"https://raw.githubusercontent.com/{owner}/{repository}/{branch}/{path}"
    return f"https://cdn.jsdelivr.net/gh/{owner}/{repository}@{commit}/{path}"


def result_payload(
    assets: list[Asset],
    owner: str,
    repository: str,
    branch: str,
    target_dir: str,
    url_mode: str,
    commit: str | None,
    pushed: bool,
) -> dict[str, object]:
    items = []
    for asset in assets:
        url = None
        if commit:
            url = build_url(
                owner,
                repository,
                branch,
                commit,
                target_dir,
                asset.target_name,
                url_mode,
            )
        items.append(
            {
                "source": str(asset.source),
                "target": PurePosixPath(target_dir, asset.target_name).as_posix(),
                "sha256": asset.digest,
                "url": url,
                "markdown": f"![{asset.source.stem}]({url})" if url else None,
            }
        )
    return {
        "repository": f"{owner}/{repository}",
        "branch": branch,
        "commit": commit,
        "pushed": pushed,
        "assets": items,
    }


def upload(args: argparse.Namespace) -> dict[str, object]:
    owner, repository, remote = parse_repo(args.repo)
    target_dir = validate_target_dir(args.target_dir)
    with tempfile.TemporaryDirectory(prefix="upload-blog-images-") as temp_text:
        temp = Path(temp_text)
        prepared_dir = temp / "prepared"
        prepared_dir.mkdir()
        assets = prepare_assets(
            args.files,
            prepared_dir,
            args.prefix,
            args.optimize_raster,
            args.quality,
        )
        if not args.push:
            return result_payload(
                assets,
                owner,
                repository,
                args.branch,
                target_dir,
                args.url_mode,
                commit=None,
                pushed=False,
            )

        repo_dir = temp / "repo"
        run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--filter=blob:none",
                "--sparse",
                "--branch",
                args.branch,
                "--single-branch",
                remote,
                str(repo_dir),
            ]
        )
        target_root = repo_dir / target_dir
        target_root.mkdir(parents=True, exist_ok=True)
        relative_targets: list[str] = []
        for asset in assets:
            relative = PurePosixPath(target_dir, asset.target_name).as_posix()
            shutil.copy2(asset.prepared, repo_dir / relative)
            relative_targets.append(relative)

        run(["git", "add", "--sparse", "--", *relative_targets], cwd=repo_dir)
        staged = subprocess.run(
            ["git", "diff", "--cached", "--quiet"], cwd=repo_dir
        ).returncode
        if staged not in {0, 1}:
            raise RuntimeError("Unable to inspect staged image changes")
        if staged == 1:
            run(["git", "commit", "-m", args.commit_message], cwd=repo_dir)
            run(["git", "push", "origin", args.branch], cwd=repo_dir)

        commit = run(["git", "rev-parse", "HEAD"], cwd=repo_dir)
        return result_payload(
            assets,
            owner,
            repository,
            args.branch,
            target_dir,
            args.url_mode,
            commit=commit,
            pushed=staged == 1,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Upload blog images to GitHub and print immutable CDN URLs."
    )
    parser.add_argument("files", nargs="+", help="Local image files to upload")
    parser.add_argument("--repo", default="xcxyh/xcxyh.github.io")
    parser.add_argument("--branch", default="image-save")
    parser.add_argument("--target-dir", default="images")
    parser.add_argument("--prefix", default=dt.date.today().strftime("%Y%m%d"))
    parser.add_argument("--commit-message", default="Add blog image assets")
    parser.add_argument(
        "--url-mode",
        choices=["jsdelivr-commit", "raw-branch"],
        default="jsdelivr-commit",
    )
    parser.add_argument(
        "--optimize-raster",
        action="store_true",
        help="Convert PNG/JPEG inputs to WebP before hashing and upload",
    )
    parser.add_argument("--quality", type=int, default=86)
    parser.add_argument(
        "--push",
        action="store_true",
        help="Perform the remote clone, commit, and push; otherwise only print a plan",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if not 1 <= args.quality <= 100:
        parser.error("--quality must be between 1 and 100")
    try:
        payload = upload(args)
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
