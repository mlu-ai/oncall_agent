## Why

项目尚无可运行、可验证且不会泄露配置的工程基础。先建立统一的目录、依赖、质量门禁和配置边界，才能让后续认证、聊天、知识库、AIOps 与 MCP 提案在可控边界内演进。

## What Changes

- 建立 npm workspaces 单体仓库骨架：Python 后端、Vue 桌面 Web 前端、API 合同包、文档、配置、基础设施说明与脚本目录。
- 锁定后端、Agent/AI、前端、文档与提交规范的技术栈和质量基线；Agent/AI 依赖只作为后续能力的边界，不实现产品功能。
- 提供最小 `/health` 应用工厂、类型化合同入口、前端页面与可执行的构建、类型检查、测试和静态检查命令。
- 建立本地 JSON 配置的递归深合并与前端公开字段 allowlist，禁止把密钥和运行时集成连接带入导入阶段或浏览器包。
- 固化 Compose 仅承载基础设施、应用与官方 CLS MCP Server 仅主机运行的部署边界。

## Capabilities

### New Capabilities

- `secure-monorepo-foundation`：提供项目目录、可运行质量命令、本地配置安全边界、导入安全性及基础设施职责边界。

### Modified Capabilities

无。

## Impact

- 新增根级 npm workspace、Python `uv` 项目、Vue/Vite 项目、合同包、VitePress 文档及项目指南。
- 新增 Python、Node.js 依赖锁定文件和本地模板配置；不会新增认证、聊天、知识库、AIOps、LLM、Milvus 或 MCP 产品接口。
- 后续提案必须遵守本次定义的目录、配置公开面、依赖注入、租户和真实外部集成规则。
