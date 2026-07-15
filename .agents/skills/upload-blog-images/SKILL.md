---
name: upload-blog-images
description: Upload one or more blog images to the project's GitHub image host, optionally convert large PNG/JPEG files to WebP, name assets with content hashes, push them to the image-save branch, and return immutable jsDelivr URLs plus Markdown. Use when Codex needs to upload, host, publish, or replace local image references in Hexo/Markdown articles in this project.
---

# Upload blog images

Upload image assets to `xcxyh/xcxyh.github.io`, branch `image-save`, directory `images/`. Return jsDelivr URLs pinned to the upload commit.

## Workflow

1. Confirm that the user explicitly requested an upload before changing the remote repository. A request such as “上传这些图片” is sufficient. Otherwise run only the dry-run.
2. Inspect the files. Keep SVG as SVG. Convert large photographic PNG/JPEG files to WebP when smaller output is useful; do not blindly convert diagrams, animated images, or files that need lossless pixels.
3. Run a dry-run first. It validates inputs and prints the content-hashed target names without network or Git changes.
4. Run again with `--push` after the plan is sound. The script uses a shallow partial clone, commits only the named assets, pushes `image-save`, and prints JSON containing commit-pinned URLs and Markdown.
5. Verify every returned URL responds with HTTP 200 and an `image/*` content type before editing an article.
6. Replace local Markdown image paths with the returned URLs. Render the Hexo draft and confirm the generated HTML contains those URLs.

## Commands

From the project root:

```bash
# Safe preview: no clone, commit, or push
python3 .agents/skills/upload-blog-images/scripts/upload_to_github.py \
  path/to/cover.png path/to/diagram.svg \
  --optimize-raster

# Upload after explicit user authorization
python3 .agents/skills/upload-blog-images/scripts/upload_to_github.py \
  path/to/cover.png path/to/diagram.svg \
  --optimize-raster --push
```

`--optimize-raster` requires Pillow. If the current Python lacks Pillow, use the Codex workspace-dependency Python or prepare the WebP separately, then upload without that flag.

Useful overrides:

```bash
--repo owner/repository
--branch image-save
--target-dir images
--prefix 20260715
--commit-message "Add article illustrations"
--url-mode jsdelivr-commit|raw-branch
```

Use `jsdelivr-commit` unless the user asks for the existing raw GitHub convention. Commit-pinned URLs are immutable, so never overwrite uploaded filenames; upload a new content hash instead.

## Output and safety

- Treat a successful Git push as an external state change and report the repository, branch, commit, and URLs.
- Do not delete local source images. They may be needed for later edits.
- Do not use Git LFS for blog images; public image URLs may resolve to pointer files instead of the image.
- If push is rejected because the branch advanced, rerun the command to clone the new head. Do not force-push.
- The script does not edit Markdown. Apply returned URLs only after verification.
