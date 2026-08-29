# 基础设施边界

最终 Compose 仅承载 etcd、MinIO、Milvus、Attu 和 Alertmanager。后端、前端及官方 CLS MCP Server 必须在主机运行。

此目录目前只记录边界，不包含应用 Dockerfile、`project.compose.json` 或应用 Compose 服务。
