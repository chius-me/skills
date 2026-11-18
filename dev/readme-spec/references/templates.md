# 开源项目 README 参考模板库

这里收录四大典型项目类型的标准 Markdown 模板源码，可直接复制后替换 `{owner}`、`{repo}`、`{author}` 等占位符使用。若为 `chius-me` 账号下仓库，占位符默认值见 [chius-profile.md](chius-profile.md)。

> 注意：主文档为英文时，章节标题和正文应全部保持纯英文（对应的 `README.zh.md` 再用纯中文）；避免在同一个文件中中英括号混写。

---

## 模板 A：Web 应用 / Edge 服务（English Primary 示例）

适用场景：Web 应用、SaaS、Cloudflare Workers / Edge API、全栈服务。

````markdown
<div align="right">
  <a href="#readme">English</a> | <a href="./README.zh.md">简体中文</a>
</div>

<div align="center">

<img src="./public/logo.svg" width="64" height="64" alt="Logo" />

# {Project Name}

{One-line value proposition explaining what problem it solves and for whom.}

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/{owner}/{repo}?color=2ea44f)](https://github.com/{owner}/{repo}/releases/latest)
[![CI](https://github.com/{owner}/{repo}/actions/workflows/ci.yml/badge.svg)](https://github.com/{owner}/{repo}/actions)
[![Cloudflare Workers](https://img.shields.io/badge/Cloudflare-Workers-f38020?logo=cloudflare&logoColor=white)](https://workers.cloudflare.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178c6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

[Live Demo]({demo_url}) · [Documentation](./docs/architecture.md) · [Issues](https://github.com/{owner}/{repo}/issues)

</div>

<p align="center">
  <img src="./docs/screenshot.png" alt="Preview" width="85%">
</p>

## ✨ Features

- **Edge-First Performance**: Built on Cloudflare Workers + Durable Objects for low-latency global response.
- **Zero-Friction Privacy**: Ready out of the box with no signup required and configurable expiration policies.
- **Responsive UI**: Adapts cleanly across desktop and mobile with automatic light/dark theme support.

## 🚀 Quick Start

### Prerequisites
- Node.js 22+
- Package manager (`pnpm` / `npm`)

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/{owner}/{repo}.git
cd {repo}

# 2. Install dependencies and start dev server
npm install
npm run dev
```

### Deployment

```bash
# Copy and fill environment variables
cp .dev.vars.example .dev.vars

# Deploy
npx wrangler deploy
```

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `SESSION_SECRET` | Yes | - | Secret key used for session signing |
| `ALLOWED_ORIGINS` | No | `*` | Allowed CORS origins |

## 📄 License

Distributed under the [MIT License](LICENSE).

<div align="center">
  <sub>Crafted with ❤️ by <a href="{author_url}">{author}</a></sub>
</div>
````

---

## 模板 B：CLI 工具 / Docker 镜像 / 后端服务（English Primary 示例）

适用场景：命令行工具、MCP Server、Bot、容器化微服务。

````markdown
<div align="right">
  <a href="#readme">English</a> | <a href="./README.zh.md">简体中文</a>
</div>

<div align="center">

# {Project Name}

{One-line summary of what this CLI or service automates.}

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/{owner}/{repo}?color=2ea44f)](https://github.com/{owner}/{repo}/releases/latest)
[![Docker](https://img.shields.io/badge/Docker-GHCR-2496ED?logo=docker&logoColor=white)](https://github.com/{owner}/{repo}/pkgs/container/{repo})
[![CI](https://github.com/{owner}/{repo}/actions/workflows/ci.yml/badge.svg)](https://github.com/{owner}/{repo}/actions)

</div>

## ✨ Features

- **Lightweight**: Small memory footprint with predictable resource usage.
- **Flexible Distribution**: Install via Homebrew, Docker, or prebuilt binaries.
- **Safe Defaults**: Strict input validation and minimal privilege requirements.

## 🚀 Installation & Usage

### Option 1: Homebrew (macOS / Linux)

```bash
brew install {owner}/tap/{tool-name}
```

### Option 2: Docker

```bash
docker run -d \
  --name {tool-name} \
  -p 8080:8080 \
  -e PORT=8080 \
  ghcr.io/{owner}/{repo}:latest
```

### Option 3: Docker Compose

```yaml
services:
  app:
    image: ghcr.io/{owner}/{repo}:latest
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - APP_ENV=production
```

## ⚙️ CLI Options

```text
Usage: {tool-name} [options] <arguments>

Options:
  -v, --version      Print current version
  -c, --config       Path to configuration file
  -h, --help         Show help message
```

## 📄 License

Distributed under the [MIT License](LICENSE).

<div align="center">
  <sub>Crafted with ❤️ by <a href="{author_url}">{author}</a></sub>
</div>
````

---

## 模板 C：主题 / 文档站 / 个人创作（中文主文档示例）

适用场景：博客主题、设计系统、教程文档、本地化工具或个人创作项目。

````markdown
<div align="right">
  <a href="#readme">简体中文</a> | <a href="./README.en.md">English</a>
</div>

<div align="center">

# {Project Name}

{一句话阐述设计目标或解决的创作痛点，例如：为个人博客打造的单栏等宽中英文混排 Hugo 主题。}

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Hugo](https://img.shields.io/badge/Hugo-Extended%200.160+-FF4088?logo=hugo&logoColor=white)](https://gohugo.io/)
[![Demo](https://img.shields.io/badge/Demo-Online%20Preview-brightgreen)]({demo_url})

[在线预览]({demo_url}) · [作者主页]({author_url})

</div>

<p align="center">
  <img src="./images/screenshot.jpg" alt="Preview Screenshot" width="85%">
</p>

## 💡 设计理念与特色

- **中英文精细混排**：兼顾等宽西文与中文正文字形、行高和断行细节。
- **克制专注**：去除多余装饰，提供适合长文阅读的干净版式。
- **开箱即用**：内置代码高亮、分类归档、纯前端即时搜索与深浅色跟随。

## 🚀 快速上手

### 本地预览

```bash
git clone https://github.com/{owner}/{repo}.git
cd {repo}
hugo server --source exampleSite
```

访问 `http://localhost:1313` 查看效果。

### 引入现有项目

```bash
git submodule add https://github.com/{owner}/{repo}.git themes/{repo}
```

## 📄 许可证

基于 [MIT 许可证](LICENSE) 开源发布。

<div align="center">
  <sub>Crafted with ❤️ by <a href="{author_url}">{author}</a></sub>
</div>
````

---

## 模板 D：精选资源清单 (Awesome List)

适用场景：工具索引、学习路线、专题资料汇总。

````markdown
<div align="center">

# Awesome {Category}

精选 {Category} 优质资源、开源工具与实践指南。

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![License](https://img.shields.io/badge/license-CC0--1.0-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/{owner}/{repo}/pulls)

[目录](#-目录) · [贡献指南](#-贡献指南)

</div>

---

## 📑 目录

- [分类一](#-分类一)
- [分类二](#-分类二)

---

## 分类一

| 项目名称 | 说明 | 方式 / 标签 |
|---|---|---|
| [项目 A](https://example.com) | 简明客观的功能说明 | Docker |
| [项目 B](https://example.com) | 简明客观的功能说明 | CLI |

## 🤝 贡献指南

欢迎提交 PR 补充或修正内容，提交前请确保：
1. 项目保持维护，具备清晰的文档与开源协议。
2. 描述简洁客观，不包含营销宣传词汇。

## 📄 许可证

本项目采用 [CC0 1.0 Universal](LICENSE) 授权发布。

<div align="center">
  <sub>Curated with ❤️ by <a href="{author_url}">{author}</a></sub>
</div>
````
