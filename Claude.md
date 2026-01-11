# Claude Code 使用指南

[![Claude](https://img.shields.io/badge/Powered_by-Claude-0081CB?style=for-the-badge&logo=anthropic&logoColor=white)](https://claude.ai/)
[![VSCode](https://img.shields.io/badge/VSCode-1.85+-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)](https://code.visualstudio.com/)

本文档介绍如何在 Hexo 博客项目中使用 Claude Code 进行高效的博客管理和内容创作。

## 📋 目录

- [什么是 Claude Code](#什么是-claude-code)
- [环境准备](#环境准备)
- [基本使用流程](#基本使用流程)
- [博客维护任务](#博客维护任务)
- [最佳实践](#最佳实践)
- [常见问题](#常见问题)
- [进阶技巧](#进阶技巧)

## 什么是 Claude Code

Claude Code 是 Anthropic 官方的 CLI 工具，专为软件开发设计，具有以下特点：

- **智能代码助手**：理解代码上下文，提供精准的代码建议
- **多语言支持**：支持 JavaScript、TypeScript、Markdown 等多种语言
- **文件操作**：直接读取、编辑项目文件
- **任务管理**：自动创建和跟踪任务列表
- **Git 集成**：理解 Git 状态，提供版本控制建议

## 环境准备

### 1. 安装 Claude Code

```bash
# 通过 npm 安装
npm install -g @anthropic-ai/claude-code

# 或者通过 pip 安装
pip install claude-code
```

### 2. 配置 VSCode

确保已安装以下 VSCode 扩展：

- **Claude Code**：官方 Claude Code 扩展
- **GitLens**：增强 Git 功能
- **Prettier**：代码格式化
- **ESLint**：代码检查（用于 JavaScript/TypeScript）

### 3. 项目配置

```bash
# 进入项目目录
cd hexo-markdown

# 初始化 Claude Code 配置（如果需要）
claude-code init
```

## 基本使用流程

### 1. 打开项目

```bash
# 在 VSCode 中打开项目
code hexo-markdown
```

### 2. 启动 Claude Code

```bash
# 在 VSCode 中使用 Ctrl+Shift+P 打开命令面板
# 搜索 "Claude Code" 相关命令
```

### 3. 基本操作示例

```bash
# 询问问题
"如何优化 Hexo 博客的加载速度？"

# 创建新文章
"帮我创建一篇关于 Jetpack Compose 性能优化的文章"

# 修改配置
"帮我更新 _config.yml 中的网站描述"

# 检查错误
"运行 hexo server 时出现错误，帮我分析"
```

## 博客维护任务

### 1. 内容创作

#### 创建新文章

```bash
# 使用 Claude Code 创建文章模板
"创建一篇关于 Android 性能优化的技术文章，包含代码示例"
```

Claude Code 会：
- 自动创建 `source/_posts/文章标题.md`
- 生成包含 Frontmatter 的文章模板
- 添加相关的分类和标签

#### 文章编辑

```bash
# 优化现有文章
"优化《Jetpack Compose 动画详解》这篇文章的结构和表达"
"为这篇文章添加更多的代码示例和实际应用场景"
```

### 2. 配置管理

#### 主题配置

```bash
# 修改主题设置
"帮我调整 Fluid 主题的配色方案为深色模式"
"添加自定义的代码高亮主题"
"配置社交链接，添加我的 GitHub 和微博"
```

#### Hexo 配置

```bash
# 更新 Hexo 配置
"优化 _config.yml 的 URL 设置"
"配置文章永久链接格式"
"启用文章置顶功能"
```

### 3. SEO 优化

```bash
# SEO 相关任务
"为所有文章生成合适的 meta 描述"
"优化文章标题的 SEO 结构"
"生成站点地图"
"配置 Google Analytics"
```

### 4. 性能优化

```bash
# 性能优化
"压缩博客中的图片资源"
"优化 CSS 和 JavaScript 文件"
"启用 CDN 加速"
"配置缓存策略"
```

## 最佳实践

### 1. 写作流程

1. **构思阶段**
   ```
   "我想写一篇关于 Jetpack Compose 性能优化的文章，帮我规划大纲"
   ```

2. **内容创作**
   ```
   "根据大纲开始写第一部分：Compose 的性能原理"
   ```

3. **代码示例**
   ```
   "为这部分内容添加 Compose 性能监控的代码示例"
   ```

4. **优化完善**
   ```
   "检查文章的逻辑结构，确保技术准确性"
   ```

### 2. 代码规范

```bash
# 使用 Claude Code 检查代码质量
"检查所有代码块是否符合 Google 的 Kotlin 编码规范"
"优化代码注释，使其更加清晰易懂"
```

### 3. 内容管理

```bash
# 文章管理
"列出最近三个月发表的所有文章"
"统计各个分类的文章数量"
"找出可能需要更新的旧文章"
```

### 4. 版本控制

```bash
# Git 操作
"帮我提交最近的更改"
"创建一个新的分支进行主题定制"
"查看最近提交的差异"
```

## 常见问题

### 1. Claude Code 无法识别 Hexo

**问题**：Claude Code 不识别 Hexo 特定的文件结构

**解决方案**：
```bash
"这是一个 Hexo 博客项目，所有文章都在 source/_posts/ 目录下"
"主题配置在 _config.fluid.yml 中"
```

### 2. 文件路径错误

**问题**：Claude Code 找不到正确的文件路径

**解决方案**：
```bash
"Hexo 文章的 Frontmatter 必须包含 title 和 date 字段"
"文章文件名应该是：年-月-日-标题.md 格式"
```

### 3. Markdown 渲染问题

**问题**：生成的 Markdown 语法不正确

**解决方案**：
```bash
"确保使用正确的 Markdown 语法"
"代码块需要指定语言类型，如 ```kotlin"
"图片路径使用相对路径"
```

## 进阶技巧

### 1. 自定义工作流

创建 `.claude-code-workflows` 目录，定义常用的工作流：

```yaml
# workflow-new-post.yml
name: 创建新文章
description: 创建一篇新的技术博客文章
steps:
  - type: ask
    question: "请输入文章标题"
    variable: title
  - type: create
    path: "source/_posts/{{title}}.md"
    template: |
      ---
      title: {{title}}
      date: {{date}}
      categories:
      tags:
      ---

      # {{title}}

      ## 引言

      ## 正文
```

### 2. 集成其他工具

```bash
# 结合 Git 使用
"帮我创建一个提交，包含最近添加的所有文章"
"生成一个 PR 描述，说明这次更新的内容"

# 结合 CI/CD
"检查 GitHub Actions 配置文件"
"优化部署脚本"
```

### 3. 批量操作

```bash
# 批量修改文章
"为所有 2024 年的文章添加 '2024' 标签"
"批量更新文章的分类"
"检查并修复所有文章的图片链接"
```

### 4. 内容分析

```bash
# 分析博客内容
"分析我博客中最受欢迎的主题"
"统计各个技术领域的文章占比"
"生成年度写作报告"
```

## 实用命令速查

| 功能 | 命令示例 |
|------|----------|
| 创建文章 | "创建一篇关于 [主题] 的文章" |
| 优化配置 | "优化 [配置文件] 中的 [设置]" |
| 检查错误 | "为什么 [命令] 执行失败？" |
| 生成报告 | "生成博客的年度统计报告" |
| 更新主题 | "更新 Fluid 主题到最新版本" |
| 添加功能 | "为博客添加 [功能]" |

## 参考资源

- [Claude Code 官方文档](https://docs.anthropic.com/claude/code)
- [Hexo 官方文档](https://hexo.io/docs/)
- [Fluid 主题文档](https://fluid-dev.github.io/hexo-theme-fluid/)
- [VSCode Claude Code 扩展](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)

---

> 💡 **提示**：善用 Claude Code 可以显著提高博客管理效率，让你更专注于内容创作而非技术细节。