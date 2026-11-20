# 共享壳层、生态互链与工程模板

新建任何 CITY 相关网站时，直接从现有站点（`city-social-map` 或 `city-avatar`）复制并保持 **`src/styles/city-shell.css`** 与 **`src/components/city-shell/*`** 与姐妹站逐字节同步，不各写一套冲突顶栏或菜单。

## 一、已上线生态站点清单（`CITY_SITES`）

当前生态包含以下生产站点与原仓库，写入 `src/components/city-shell/ecosystem.ts`：

| `CitySiteId` | `subtitle` | 线上域名 (`url`) | GitHub 原仓 (`repoSlug` / `repoUrl`) | 强调色 |
| --- | --- | --- | --- | --- |
| `'social-map'` | `SOCIAL MAP` | `https://social.city.chius.dev` | `chius-me/city-social-map` (`https://github.com/chius-me/city-social-map`) | `#f7b647` |
| `'avatar'` | `AVATAR` | `https://avatar.city.chius.dev` | `chius-me/city-avatar` (`https://github.com/chius-me/city-avatar`) | `#f09cb4` |

### 注册第 3 个及更多新站的规范步骤

1. 在 `ecosystem.ts` 中扩展 `export type CitySiteId = 'social-map' | 'avatar' | '<new-id>';`，并在 `CITY_SITES` 与 `CITY_SITE_LIST` 中补齐中/英/日三语 `name`、`shortLabel`、`summary`、`url`、`domain`、`repoUrl`、`repoSlug`、`accent`。
2. 调整 `getSisterSite(siteId)` 指向主推姊妹站；当站内需要展示 2 个以上姊妹站时，通过 `extraLinks` 在 `.city-menu-links` 补充胶囊即可，保持右上角菜单干净不臃肿。
3. 同步更新现有 `city-*` 站点的 `ecosystem.ts` 与 `README.md` / `README.zh.md`，做到菜单内与文档双向可发现。

## 二、`components/city-shell/` 组件契约

| 组件 / 导出 | 核心 Props | 职责与视觉细节 |
| --- | --- | --- |
| `CityLogo` | `compact?: boolean`, `subtitle?: string`, `className?: string` | 四色粗黑边手写风格 C-I-T-Y 矢量字标，下方配全大写 `subtitle` 与 `<CityDots />` |
| `CityDots` | `className?: string` | `#F7B647` / `#F09CB4` / `#99CB77` / `#EE847D` 带黑边四色圆点装饰 |
| `GitHubMark` | `size?: number`, `className?: string` | 内联标准 GitHub Octocat SVG（避免跨版本 `lucide-react` 缺失品牌图标） |
| `MiminekoMascot` | `className?: string` | 白耳猫（Mimineko）矢量化看板角色，附轻快 `mimineko-bob` 摇曳 |
| `CityTopShell` | `siteId`, `locale`, `onChangeLocale`, `menuOpen`, `onToggleMenu`, `onBrandClick?`, `brandTitle?`, `children?` | 渲染极简左上品牌徽章与右上 `.city-top-shelf`（只放 `children` 工具槽 ＋ 三语切换 ＋ 菜单钮），并随语言切换自动同步 `document.title`（取 `CITY_SITES[siteId].tabTitle`）与 `<html lang>` |
| `CityMenuOverlay` | `siteId`, `open`, `locale`, `tagline`, `tiles: CityMenuTile[]`, `onClose`, `extraLinks?`, `creditNote?`, `children?` | 统一 `Escape`/点击遮罩关闭、左侧商标与吉祥物、4 枚主题色大瓷砖（支持 `onClick` 或外链 `href`）、可选紧凑插件槽 `children`（推荐最多 1 个 `.city-menu-tabs-card` + 单行 `.city-menu-kbd-hint`）、自动去重的底部胶囊行 `.city-menu-links`（自动高亮姊妹站胶囊并附带 `<GitHubMark /> GitHub ↗`、`Awesome CITY ↗`、`官方官网 ↗`）与极简版权尾注 |
| `CityLoadingCurtain` / `CityLoadingDots` | `subtitle: string` | 官网天蓝（`#1395ea`）入场遮罩（居中白底黑边卡片 + Mimineko）与四色跳跃加载点 |
| `CityFooter` | `siteId?: CitySiteId`, `locale` | 渲染干净的单行非官方/版权声明，不在主页面页脚堆积外链 |

## 三、文档头、Favicon 与 Cloudflare 部署模版

### 1. HTML `<head>`（`index.html`）与标签页标题规范

所有 `*.city.chius.dev` 网站统一标签页标题格式（静态 `<title>` / `og:title` 默认简体中文，切换语言后由 `CityTopShell` 自动同步 `CITY_SITES[siteId].tabTitle` 与 `<html lang>`）：

- **中文**：`CITY <Module> · 《小城日常》<中文模块名>`（例如 `CITY Social Map · 《小城日常》人物关系图`、`CITY Avatar · 《小城日常》风格头像工坊`）
- **English**：`CITY <Module> · CITY THE ANIMATION`
- **日本語**：`CITY <Module> · 『CITY THE ANIMATION』<日文模块名>`

统一加载 `M PLUS Rounded 1c`（400/500/700/800/900）＋ `Noto Sans SC`，补齐三端 SEO 与主题色 `#f7b647`：

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CITY <Module> · 《小城日常》<中文模块名></title>
    <meta name="description" content="..." />
    <meta property="og:title" content="CITY <Module> · 《小城日常》<中文模块名>" />
    <meta property="og:description" content="..." />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://<slug>.city.chius.dev/" />
    <link rel="canonical" href="https://<slug>.city.chius.dev/" />
    <meta name="theme-color" content="#f7b647" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&family=Noto+Sans+SC:wght@400;500;700;900&display=swap"
      rel="stylesheet"
    />
  </head>
```

### 2. 系列统一 `public/favicon.svg`

所有 CITY 网站共享同一枚图标（源自 `city-social-map`，白底黑描边 `64×64` 圆角方块＋四枚带黑边 C-I-T-Y 彩色圆点），逐字节保持一致：

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect x="3" y="3" width="58" height="58" rx="16" fill="#FFFFFF" stroke="#141419" stroke-width="5"/>
  <circle cx="21" cy="21" r="10" fill="#F7B647" stroke="#141419" stroke-width="3.2"/>
  <circle cx="43" cy="21" r="10" fill="#F09CB4" stroke="#141419" stroke-width="3.2"/>
  <circle cx="21" cy="43" r="10" fill="#99CB77" stroke="#141419" stroke-width="3.2"/>
  <circle cx="43" cy="43" r="10" fill="#EE847D" stroke="#141419" stroke-width="3.2"/>
</svg>
```

### 3. Cloudflare Workers 路由（`wrangler.jsonc`）

新站点默认接入 `*.city.chius.dev` 自定义域名并开启资产单页路由或 Worker 后端，如涉及 CI 自动部署，在 `.github/workflows/deploy.yml` 仅对 `main` 推送执行 build 与 deploy，且遵守仓库与云端凭证规范。

### 4. 中英双语 README 互链约定

配合 `readme-spec` skill 生成 `README.md` 与 `README.zh.md` 时：
- 标题下方快捷链接行必须包含本站在线域名、主要姊妹站链接（如 `[CITY Social Map](https://social.city.chius.dev)` / `[CITY Avatar](https://avatar.city.chius.dev)`）、Issues 与 `[Awesome CITY](https://github.com/chius-me/awesome-citytheanimation)`；
- `Credits & Sources` / `参考与致谢` 小节单独设一行 `- **Sister Project(s)**` 列出姊妹项目的 GitHub 仓库与线上域名。
