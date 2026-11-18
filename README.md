<div align="center">

# skills

一组用于内容写作、视觉创作、网页设计与开源文档规范的 Agent Skills 合集（兼容 Antigravity、Codex、Claude Code 及 Grok Build）。

[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![CI](https://github.com/chius-me/skills/actions/workflows/ci.yml/badge.svg)](https://github.com/chius-me/skills/actions/workflows/ci.yml)
![Skills](https://img.shields.io/badge/Skills-9-2ea44f?style=flat)

[技能目录](#技能目录) · [安装方式](#安装方式) · [本地校验](#本地校验)

</div>

---

## 技能目录

按**通用能力**与**个人/特定工具预设**分类，按需安装对应子目录即可：

### 通用技能（General-Purpose）

| 技能 | 路径 | 说明 | 外部依赖 |
| --- | --- | --- | --- |
| `blog-writing` | [`blog/blog-writing`](blog/blog-writing) | 润色中文个人博客，或从代码仓库/开发记录提炼有取舍、不杜撰的技术文章 | 无 |
| `blog-localization` | [`blog/blog-localization`](blog/blog-localization) | 校对简体中文博客，并本地化重写为台湾正体（`zh-TW`）与美式英语（`en-US`） | 无（静态站点验证按项目而定） |
| `colorblock-editorial` | [`creation/colorblock-editorial`](creation/colorblock-editorial) | 大色块、衬线标题与单主体的杂志编辑风封面、海报及系列图文设计 | 图像生成或排版工具 |
| `benchmark-showcase` | [`creation/benchmark-showcase`](creation/benchmark-showcase) | 大窗演示、细节卡片、同题双栏和榜单动效，用于模型横评及产品对比视频 | 分镜无工具依赖，渲染沿用项目工具 |
| `place-plate` | [`creation/place-plate`](creation/place-plate) | 保留原照片，基于真实字体度量渲染地名、细白描线、引线与区位简图 | Python 3 + Pillow |
| `readme-spec` | [`dev/readme-spec`](dev/readme-spec) | 标准化开源项目 README（30 秒法则、Hero 头部、Badges 与可复现命令；附可选 `chius-me` 预设） | 无 |

### 品牌预设与特定运行时技能（Brand Presets & Runtime-Specific）

| 技能 | 路径 | 说明 | 适用范围 / 依赖 |
| --- | --- | --- | --- |
| `swiss-style` | [`design/swiss-style`](design/swiss-style) | 纸感等宽瑞士网格网页设计系统，内置 `chius.me` 与 `chius.cc`（Chipaper）参考预设 | 通用纸感等宽网格 / Chius 品牌站 |
| `motion-explainer` | [`creation/motion-explainer`](creation/motion-explainer) | 按 Chius 的编导偏好，从选题调查和中文脚本到可审的动态图解样片与成片 | 写稿无工具依赖，渲染沿用项目工具，抽帧需 Python 3 与 FFmpeg |
| `grok-collage-broll` | [`creation/grok-collage-broll`](creation/grok-collage-broll) | 5–6 秒短口播转 9:16 半调纸拼贴无声 B-roll，含三阶段审批闸门与路径对照实验 | Grok Build（`image_gen` / `reference_to_video`）+ `ffmpeg` |

---

## 安装方式

本仓库按类别分两级目录存放，建议只将需要的 `<category>/<skill-name>` 复制或软链接到对应 Agent 的 skills 目录中，避免嵌套路径无法被自动扫描。

```bash
git clone https://github.com/chius-me/skills.git
cd skills
```

### 安装单个通用技能

```bash
# 示例：安装到 Codex / Antigravity / Claude Code（按实际工具目录二选一）
cp -R creation/place-plate ~/.codex/skills/place-plate
# 或项目内使用：
# cp -R blog/blog-writing .agents/skills/blog-writing
```

### 安装 `grok-collage-broll`（仅运行时所需文件）

`creation/grok-collage-broll/experiments/` 存放方案对照报告与采样对比图。安装到 Agent 运行目录时可排除该目录以保持轻量：

```bash
mkdir -p ~/.grok/skills/grok-collage-broll
rsync -a --exclude 'experiments/' creation/grok-collage-broll/ ~/.grok/skills/grok-collage-broll/
bash ~/.grok/skills/grok-collage-broll/scripts/check_setup.sh
```

---

## 本地校验

运行仓库结构、链接有效性及各脚本的单元测试：

```bash
# 1. 全库 Frontmatter、目录名一致性与 Markdown 链接检查
python3 scripts/validate_repo.py

# 2. place-plate 渲染与校验单元测试（需 Pillow）
python3 -m unittest discover -s creation/place-plate/scripts -p 'test_*.py'

# 3. grok-collage-broll 结构与 ffmpeg 冒烟测试（需 ffmpeg / ffprobe）
bash creation/grok-collage-broll/scripts/verify_skill.sh
```

---

## 许可证

本仓库基于 [MIT License](LICENSE) 开源发布。[`creation/grok-collage-broll`](creation/grok-collage-broll) 保留其上游衍生自 `pyang5166/gbro-collage-broll` 的原始 [MIT License](creation/grok-collage-broll/LICENSE) 版权声明。
