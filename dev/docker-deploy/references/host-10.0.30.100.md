# 10.0.30.100 的运行约定

项目位于 `/opt/<name>/`，在项目目录运行 Compose。主机重启后由容器的 restart policy 恢复服务，没有按项目拆分的 systemd 单元。

## Compose 文件

- 主文件统一命名为 `docker-compose.yaml`，省略 `version`。顶层依次写 `name`、`x-*`、`services`、`networks`、`volumes`。已有项目的 `name` 取运行中的 Compose 项目名。`/opt/reactive-resume` 对应 `reactive_resume`。
- 服务字段依次写 `image`、`container_name`、`hostname`、`restart`、`network_mode` 或 `networks`、`depends_on`、`env_file`、`environment`、`ports`、`volumes`，之后放 `command` 和安全相关字段，最后放 `healthcheck`。
- 每个服务写明 `image`、`container_name` 和 `restart`。使用 `restart: unless-stopped`。Dify 的 `init_permissions` 保留 `restart: "no"`，退出码 0 表示正常完成。
- 日志沿用 `/etc/docker/daemon.json` 的 `json-file`，单文件 20m，保留 3 个。Compose 中省略 `logging` 和 `x-logging`。
- Supabase 的所有 Compose 操作均同时传入 `-f docker-compose.yaml -f docker-compose.logs.yml`。
- Glance 的 `/opt/glance` 指向 `/opt/.glance-deploy/releases/<当前发布>`。编辑该链接指向的发布文件。每次重建前读取当前 `/opt/glance/.revision`，将其值作为 `GLANCE_DEPLOY_REVISION` 传给 Compose，并核对容器标签 `io.tamochi.glance.config-revision`。

## 网络

单容器且无需容器间名称解析时，使用 `network_mode: bridge` 接入 docker0。保留 `network_mode: host` 的服务只有 frpc、SakuraFRP 和 Glance 的 komga-proxy、navidrome-proxy。

多容器项目使用一个桥接网络，在 Compose 中显式声明 `/24`。Dify 保留 dify、dify-ssrf、dify-agent 三个隔离网络。保留现有显式网段；新建网络从 `172.18.0.0/16` 中按 size 24 分配，每次以实时网络和路由为准。

下表记录 2026-11-24 的分配。比如第三段为 2 表示 `172.18.2.0/24`。

| 第三段 | 网络或项目 | 第三段 | 网络或项目 |
| --- | --- | --- | --- |
| 0 | traccar（gps） | 10 | wordpress |
| 1 | 当时空闲 | 11 | romm |
| 2 | reactive-resume | 12 | langfuse |
| 3 | searxng | 13 | dawarich |
| 4 | prometheus-grafana | 14 | supabase |
| 5 | omniroute_default | 15 | glance |
| 6 | outline | 16 | dify-ssrf |
| 7 | authentik | 17 | dify-agent |
| 8 | paperless-net | 18 | docker0 |
| 9 | dify | 19 | 当时空闲 |

## 镜像与恢复

- `local/glance-bilibili` 是未发布的本地镜像，跳过拉取。GHCR 拉取曾因并发而停滞，保持串行。
- containerd ingest 多次观察均无进展时，如需清理 lease，仅处理能确认属于本次停滞拉取、在 `moby` 命名空间且带 `containerd.io/gc.expire` 的 lease。保留容器 lease 和归属不明的 lease。
- 2026-11-24 的数据库基线是 Reactive Resume 使用 `postgres:19`，Paperless 和 Outline 使用 `postgres:18`，主机上没有 `postgres:latest` 标签。保留固定主版本，操作前核对实际配置。
- 重建 Paperless 的 webserver 前，先记录并暂停 Traccar 正在运行的 autoheal。webserver 健康后恢复原先运行的 autoheal 并核对其状态。若 webserver 仍不健康，报告故障及 autoheal 的暂停状态。迁移已写入数据库时禁止退回旧镜像。
