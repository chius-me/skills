# Shields.io 徽标规范与速查表

为保持风格统一，所有徽标一律遵循以下格式约定。使用时将 `{owner}` 与 `{repo}` 替换为目标仓库的 GitHub 所有者与仓库名（`chius-cc` 预设见 [chius-profile.md](chius-profile.md)）。

---

## 1. 核心约定

- **参数统一**：使用默认的 `style=flat`（扁平风格）。
- **必须可点击**：每个徽标尽量附带明确的超链接跳转（指向 `LICENSE`、Releases、Actions 或官方站点），避免死链或装饰性堆砌。
- **左标题与右文案**：标签（label）简短，信息（message）精确；总数量控制在 4～6 个。

---

## 2. 常用徽标公式

### 2.1 许可证 (License)
```markdown
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![License](https://img.shields.io/badge/license-CC0--1.0-blue.svg)](LICENSE)
```

### 2.2 版本号 (Latest Release)
```markdown
[![Release](https://img.shields.io/github/v/release/{owner}/{repo}?color=2ea44f)](https://github.com/{owner}/{repo}/releases/latest)
```

### 2.3 工作流 / CI 状态 (GitHub Actions)
```markdown
[![CI](https://github.com/{owner}/{repo}/actions/workflows/ci.yml/badge.svg)](https://github.com/{owner}/{repo}/actions)
[![Docker](https://github.com/{owner}/{repo}/actions/workflows/docker.yml/badge.svg)](https://github.com/{owner}/{repo}/actions)
[![Pages](https://github.com/{owner}/{repo}/actions/workflows/pages.yml/badge.svg)](https://github.com/{owner}/{repo}/actions)
```

### 2.4 平台与生态 (Platform)
```markdown
[![Cloudflare Workers](https://img.shields.io/badge/Cloudflare-Workers-f38020?logo=cloudflare&logoColor=white)](https://workers.cloudflare.com/)
[![Docker GHCR](https://img.shields.io/badge/Docker-GHCR-2496ED?logo=docker&logoColor=white)](https://github.com/{owner}/{repo}/pkgs/container/{repo})
[![Homebrew](https://img.shields.io/badge/Homebrew-Tap-FBB040?logo=homebrew&logoColor=white)](https://brew.sh/)
[![Hugo](https://img.shields.io/badge/Hugo-Extended%200.160+-FF4088?logo=hugo&logoColor=white)](https://gohugo.io/)
```

### 2.5 开发语言 (Language)
```markdown
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178c6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Go](https://img.shields.io/badge/Language-Go-00ADD8?logo=go&logoColor=white)](https://go.dev/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776ab?logo=python&logoColor=white)](https://www.python.org/)
```
