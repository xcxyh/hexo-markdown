# Xiong's Blogs

[![Hexo](https://img.shields.io/badge/Hexo-7.3.0-0E83CD?style=for-the-badge&logo=hexo&logoColor=white)](https://hexo.io/)
[![Theme](https://img.shields.io/badge/Theme-Fluid-1.9.7-42B883?style=for-the-badge&logo=hexo&logoColor=white)](https://github.com/fluid-dev/hexo-theme-fluid)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

个人技术博客，基于 Hexo + Fluid 搭建，分享 Android 开发、Jetpack Compose、AI 技术等干货内容。

## 🌐 在线访问

[**https://vnipanda.xyz/**](https://vnipanda.xyz/)

## 📋 项目介绍

这是一个使用 Hexo 7.3.0 和 Fluid 1.9.7 搭建的现代化个人技术博客，主要用于分享：

- **Android 开发**：Jetpack Compose、Android 性能优化、框架源码分析
- **前端技术**：Hexo 博客搭建、工具使用技巧
- **AI 应用**：AI 生图变现、Claude Code 实战经验
- **编程语言**：C++、Java 等编程语言实践

## 🚀 技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| **Hexo** | 7.3.0 | 静态站点生成器 |
| **Fluid** | 1.9.7 | 现代化博客主题 |
| **Node.js** | - | 运行环境 |
| **Git** | - | 版本控制 |
| **pnpm** | - | 包管理器 |

## 📁 项目结构

```
hexo-markdown/
├── _config.yml          # Hexo 主配置文件
├── _config.fluid.yml    # Fluid 主题配置
├── source/_posts/       # 文章源码（20+ 篇技术文章）
├── scaffolds/           # 文章模板
├── themes/              # 主题文件（通过 npm 安装）
└── public/              # 生成的静态文件
```

## 🛠️ 核心特性

- **✨ 现代化主题**：使用 Fluid 主题，支持响应式设计、深色模式
- **📝 Markdown 写作**：简洁的 Markdown 格式，专注内容创作
- **⚡ 快速渲染**：Hexo 高效渲染，秒级生成静态页面
- **🎨 代码高亮**：支持多种编程语言代码高亮与复制
- **🏷️ 分类标签**：完善的文章分类和标签系统
- **🚀 自动部署**：一键部署至 GitHub Pages
- **📱 SEO 友好**：内置 SEO 优化，支持站点地图

## 📝 最新文章

### 2025年
- [《从一条小红书爆帖到 AI 生图变现》](source/_posts/在中国，稳定好用的-AI-coding-工具和模型.md) - 2025-12-21
- [《低成本使用 claude-code》](source/_posts/低成本使用-claude-code.md) - 2024-11-15

### 热门文章
- [《AirBnb-Mavericks - Android 原生优雅组件化框架》](source/_posts/AirBnb-Mavericks-Android-原生优雅组件化框架.md)
- [《Jetpack Compose 动画详解》](source/_posts/Jetpack-Compose-动画详解.md)
- [《Android 键盘高度监听方案》](source/_posts/Android-键盘高度监听方案.md)
- [《Hexo + Fluid 搭建个人博客》](source/_posts/Hexo-Fluid-搭建个人博客.md)

## 🚀 快速开始

### 环境要求

- Node.js >= 14.0.0
- Git
- pnpm（推荐）

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/xcxyh/hexo-markdown.git
   cd hexo-markdown
   ```

2. **安装依赖**
   ```bash
   pnpm install
   ```

3. **启动本地服务**
   ```bash
   hexo server
   ```

4. **访问博客**
   打开浏览器访问 [http://localhost:4000](http://localhost:4000)

### 写作新文章

```bash
# 创建新文章
hexo new post "文章标题"

# 创建草稿
hexo new draft "草稿标题"

# 发布草稿
hexo publish draft "草稿标题"
```

## 📊 博客统计

- **文章总数**：20+ 篇
- **分类数量**：6 个主要分类
- **标签数量**：50+ 个标签
- **更新频率**：保持月度更新

## 🎨 主题定制

Fluid 主题提供了丰富的自定义选项，主要通过 `_config.fluid.yml` 配置：

- **配色方案**：支持多种预设配色
- **代码高亮**：可配置代码主题和样式
- **社交链接**：自定义社交媒体图标
- **评论系统**：支持 Disqus、Gitalk 等

## 🚀 部署说明

本项目已配置自动部署至 GitHub Pages：

1. **推送代码**
   ```bash
   git add .
   git commit -m "更新博客内容"
   git push origin main
   ```

2. **自动构建**
   GitHub Actions 会自动构建并部署到 Pages

## 📝 许可证

[MIT License](LICENSE) - 详见 [LICENSE](LICENSE) 文件

## 🤝 联系方式

- **博客**：[https://vnipanda.xyz/](https://vnipanda.xyz/)
- **GitHub**：[@xcxyh](https://github.com/xcxyh)
- **邮箱**：[window3cc@qq.com](mailto:window3cc@qq.com)

---

> 🌟 如果这个博客项目对你有帮助，请考虑给个 Star！