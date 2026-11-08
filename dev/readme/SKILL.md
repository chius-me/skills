---
name: readme-spec
description: 规范化并撰写高质量开源项目 README。适用于 chius-me 账号下的公开仓库门面标准化、双语导航配置、Shields.io 徽章排版、核心特性提炼及安装运行指引。
---

# 开源项目 README 规范标准

为开源项目打造统一、克制、富有工程师美感且具备高转化率的门面。兼顾「30 秒看懂价值」与「60 秒快速上手」。

完整的四大项目类型模板见 [参考模板库](references/templates.md)，徽标参数速查表见 [Shields 徽标规范](references/badges.md)。

---

## 1. 核心设计原则

- **30 秒法则（The 30-Second Rule）**：访客进入仓库首页，首屏必须解答三个问题：这是什么？解决了什么痛点？怎么跑起来？
- **克制与审美**：
  - 拒绝大段纯文字堆砌，善用表格、列表与终端代码块。
  - 徽章数量控制在 4～6 个（版本、许可证、运行平台、开发语言、CI 状态），不盲目堆砌。
  - 具有 Web/GUI/终端视觉输出的项目，首屏必须提供 Demo 链接或高清预览截图。
- **中文本位，兼顾国际化**：
  - 国际通用工具（Worker 应用、CLI、开发组件）主文档 `README.md` 为美式英文，配备 `README.zh.md`。
  - 中文本土项目（博客主题、中文资源列表、参赛作品）主文档 `README.md` 为中文，按需配备 `README.en.md`。
  - 无论以哪种语言为主，页面右上角统一设置双语切换锚点。
- **真实可复现**：快速开始命令必须最小闭环，杜绝缺少依赖声明或命令无法复制执行的情况。

---

## 2. 标准骨架规范 (Standard Anatomy)

正文按照以下固定骨架顺序展开（根据项目性质可增删非核心章节，但骨架顺序保持一致）：

```text
1. 语言切换器 (Language Switcher - 右对齐)
2. Hero 头部 (居中 Logo + 项目名称 + Slogan + 规范徽标 + 核心链接)
3. 视觉预览 (Demo / Screenshot / Terminal GIF - 居中)
4. ✨ 特性列表 (Features - 4~8 个核心亮点，Emoji + 加粗标题 + 简要展开)
5. 🚀 快速开始 (Quick Start - 前置要求 + 最小运行命令)
6. 💡 使用指南 / 部署方式 (Usage / Deployment - CLI 命令 / Docker / Wrangler)
7. ⚙️ 配置说明 (Configuration - 环境变量表格)
8. 🏗️ 架构与设计 (Architecture - 可选，技术选型或流程图)
9. 📄 许可证 & 页脚 (License & Footer)
```

---

## 3. 排版细节要求

### 3.1 头部 Hero Header
统一采用居中 HTML 块，包含项目 Logo（如有，推荐 56px~64px 矢量图）、标题、1～2 句痛点描述、精选徽标栏与直达链接：

```html
<div align="right">
  <a href="#readme">English</a> | <a href="./README.zh.md">简体中文</a>
</div>

<div align="center">

<img src="./public/logo.svg" width="60" height="60" alt="Logo" />

# 项目名称

一句话痛点描述，清晰点出项目的核心能力与应用场景。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/chius-me/{repo}?color=2ea44f)](https://github.com/chius-me/{repo}/releases/latest)
[![CI](https://github.com/chius-me/{repo}/actions/workflows/ci.yml/badge.svg)](https://github.com/chius-me/{repo}/actions)
[![Platform](https://img.shields.io/badge/Cloudflare-Workers-f38020?logo=cloudflare&logoColor=white)](https://workers.cloudflare.com/)

[在线演示](https://demo.example.com) · [问题反馈](https://github.com/chius-me/{repo}/issues) · [更新日志](https://github.com/chius-me/{repo}/releases)

</div>

---
```

### 3.2 徽标规范（Badges）
- 必须使用 `style=flat`（简洁扁平风格）。
- 每个 Badge 必须带有可点击的有效目标链接（如 License 指向 `LICENSE`，Release 指向 releases，CI 指向 actions 页面）。
- 常用颜色规范：
  - 许可证 (MIT)：`blue`
  - 最新版本 (Release)：`2ea44f`
  - Cloudflare：`f38020`
  - Go：`00ADD8`
  - TypeScript：`3178c6`
  - Python：`3776ab`
  - Docker：`2496ED`
  - Hugo：`FF4088`

### 3.3 快速开始（Quick Start）
- 必须明确给出 `前置依赖`（如 Node 22+、Docker 24+、pnpm 10+）。
- 命令采用独立的代码块，按序标号或分步呈现：
  ```bash
  # 1. 克隆代码
  git clone https://github.com/chius-me/{repo}.git
  cd {repo}

  # 2. 安装与运行
  npm install
  npm run dev
  ```

### 3.4 优雅页脚 (Footer)
文档结尾统一附带个人署名与站点链接：

```markdown
---

## 📄 License

Distributed under the [MIT](LICENSE) License.

<div align="center">
  <sub>Crafted with ❤️ by <a href="https://chius.cc">Chius</a> · Powered by Cloudflare & GitHub</sub>
</div>
```

---

## 4. 四大项目类型分类对照

在重构或新建 README 时，先对项目进行归类，再套用对应的模板：

| 类型 | 典型项目 | 核心侧重点 | 推荐主语言 |
|---|---|---|---|
| **A: Web / Worker 服务** | `ilist`, `live-clip`, `piik-worker`, `geomuse`, `uptime-worker` | 在线体验链接、架构流图、Durable Objects 交互、Wrangler 部署与环境变量表 | 英文 (工具类) / 中文 (科普或个人) |
| **B: CLI / Docker / 服务** | `favicon-fisher`, `qbittorrent-bot`, `minecraft-admin-mcp`, `comfy-helper`, `mcd-spec` | Homebrew 安装、Docker Compose 配置、命令行参数表、安全权限模型 | 英文 (国际开源) / 中文 (本土比赛) |
| **C: 主题 / 博客 / 创作** | `chipaper`, `sks3200-8e2x-doc`, `franklin-house`, `tamako-market-s2` | 视觉效果大图、排版审美、中英文等宽字体混排说明、子模块引入步骤 | 中文优先 |
| **D: 精选列表 (Awesome)** | `awesome-selfhosted-cn`, `awesome-ghibli-images`, `awesome-nichijou` | 目录跳转锚点、精选标准、项目表格对比、PR 贡献准则 | 中文 / 双语 |

---

## 5. 验收清单 (Checklist)

修改或创建完成后逐项检查：
1. **语言锚点**：右上角是否有双语切换链接？目标文件是否存在且路径正确？
2. **居中头部**：是否包含项目名称、精炼一句话描述以及 4~6 个格式统一的徽标？
3. **视觉展示**：有界面的项目是否提供了预览图？图片路径是否能在 GitHub 正常渲染？
4. **命令闭环**：快速开始命令能否直接在全新机器上复制运行？
5. **协议声明**：是否明确标出 MIT / CC0，且与仓库根目录的 `LICENSE` 文件一致？
6. **页脚统一**：底部是否包含署名与个人主页链接？
