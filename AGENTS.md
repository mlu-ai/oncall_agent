# 项目指南

## 目录与命令

- `apps/backend` 是 Python 后端；在该目录运行 `uv sync`、`uv run ruff check .`、`uv run pyright`、`uv run pytest`。
- `apps/frontend` 是 Vue 桌面 Web；根 npm scripts 提供 `frontend:dev`、`frontend:typecheck`、`frontend:test`、`frontend:build`。
- `packages/api-contracts` 是共享 TypeScript 合同；根 npm scripts 提供 `contracts:typecheck`、`contracts:test`。`docs` 使用 VitePress，根 scripts 提供 `docs:dev`、`docs:build`。
- 使用 npm workspaces、uv 和 Conventional Commits；不要引入第二个 JS 或 Python 包管理器。

## Python 与依赖注入

- Python >=3.10，包仅位于 `apps/backend/src/super_ai`；只写 `from super_ai...`，绝不写 `from src.super_ai...`。后端栈固定为 FastAPI、Pydantic v2、uv、hatchling、src layout、SQLAlchemy 2 async、aiosqlite、Alembic、pytest、pytest-asyncio、Ruff 与 strict Pyright。
- 使用 FastAPI 应用工厂和显式依赖注入。模块导入不得连接 SQLite、Milvus、LLM 或 MCP；真实连接只在后续提案的受控启动路径中创建。
- 保持 pytest `asyncio_mode=auto`、Ruff line-length 100 / py310 / B,E,F,I,UP 与 strict Pyright。

## 配置与凭据

- 只提交 `config/*.template.json`；`project.json` 与 `user.project.json` 是被忽略的本机文件。项目配置只读取这两份本地 JSON 的递归深合并，不使用 OS 环境变量作为项目配置。
- 前端仅接收 allowlist：标题、API 基地址和明确公开的 analytics key。LLM、CLS、MCP、MinIO 及任意密钥不得进入浏览器 bundle。
- 测试创建临时配置，不能依赖或读取开发者真实配置与凭据。

## 租户与真实集成

- 后续每个业务入口都必须显式携带并校验 tenant 上下文，不以全局默认租户替代。
- 真实 LLM、Milvus、MCP、CLS 与对象存储集成只能在其专门 OpenSpec 提案中实现；foundation 不提供伪生产连接。

## OpenSpec 与运行边界

- OpenSpec 工件一律使用简体中文并遵循 spec-driven 工作流；实施前读 proposal、spec、design、tasks，归档前验证并同步 delta specs。
- Compose 最终仅托管 etcd、MinIO、Milvus、Attu、Alertmanager。后端、前端和官方 CLS MCP Server 均在主机运行；不创建应用 Dockerfile、`project.compose.json` 或应用 Compose 服务。
- 前端以桌面 Web 验收；任何 UI 变更都至少运行 typecheck、test、build。
- 前端栈固定为 Vue 3.5、Vite 6、TypeScript 5.6 strict（`exactOptionalPropertyTypes`、`noUncheckedIndexedAccess`、`isolatedModules`、ES2022/Bundler resolution）、Pinia 3、Vue Router 4、Vitest 2、marked、DOMPurify、lucide-vue-next。后续 Agent/AI 栈固定为 LangChain 1.x `create_agent`、LangGraph、langchain-openai、langchain-mcp-adapters、MCP、pymilvus 3、rank-bm25、pypdf、langchain-text-splitters、httpx。
