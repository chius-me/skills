# chius-n 个人配置预设（可选）

当目标仓库属于 `chius-n` 账号或作者显式要求沿用 Chius 个人风格时，按本预设替换通用模板中的占位符。其他开源项目直接保留通用占位符或使用项目自身信息即可。

## 默认身份与链接

| 占位符 | 默认值 | 说明 |
| --- | --- | --- |
| `{owner}` | `chius-n` | GitHub 账号或组织名 |
| `{author}` | `Chius` | 署名名称 |
| `{author_url}` | `https://chius.cc` | 个人主页 |
| `{demo_url}` | `https://{domain}.chius.dev` 或 `https://demo.chius.cc` | 在线演示地址 |
| `{footer}` | `Crafted with ❤️ by <a href="https://chius.cc">Chius</a>` | 居中页脚署名 |

## 典型项目归类参考

| 类型 | 典型项目 | 核心侧重点 | 推荐主语言 |
| --- | --- | --- | --- |
| **A: Web / Worker 服务** | `ilist`, `live-clip`, `piik-worker`, `geomuse`, `uptime-worker` | 在线体验链接、架构流图、Durable Objects 交互、Wrangler 部署与环境变量表 | 英文（工具类）/ 中文（科普或个人） |
| **B: CLI / Docker / 服务** | `favicon-fisher`, `qbittorrent-bot`, `minecraft-admin-mcp`, `comfy-helper`, `mcd-spec` | Homebrew 安装（`brew install chius-n/tap/{tool}`）、Docker Compose 配置、命令行参数表、安全权限模型 | 英文（国际开源）/ 中文（本土比赛） |
| **C: 主题 / 博客 / 创作** | `chipaper`, `sks3200-8e2x-doc`, `franklin-house`, `tamako-market-s2` | 视觉效果大图、排版审美、中英文等宽字体混排说明、子模块引入步骤 | 中文优先 |
| **D: 精选列表 (Awesome)** | `awesome-selfhosted-cn`, `awesome-ghibli-images`, `awesome-nichijou` | 目录跳转锚点、精选标准、项目表格对比、PR 贡献准则 | 中文 / 双语 |
