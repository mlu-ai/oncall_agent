## Context

这是空仓库的首个变更。实现必须满足 `proposal.md` 与 `secure-monorepo-foundation` 规格，并为后续多个产品提案建立稳定边界，而不预先实现产品能力。

## Goals / Non-Goals

**Goals:**

- 建立最终目录：`apps/backend`、`apps/frontend`、`packages/api-contracts`、`config`、`infra`、`scripts`、`openspec`、`docs`。
- 让每个工作区能在本机独立安装、类型检查、测试和构建；桌面 Web 是前端验收目标。
- 在第一天建立本地 JSON 配置、模板、忽略规则、后端深合并和前端 allowlist 的安全边界。

**Non-Goals:**

- 不实现认证、聊天、知识库、AIOps、真实 LLM、Milvus、MCP、CLS 或对象存储交互。
- 不提供应用 Dockerfile、`project.compose.json` 或任何应用 Compose 服务。
- 不设计历史密钥清理、`filter-repo` 或 force push 流程。

## Decisions

### 单体仓库与技术栈

根目录使用 npm workspaces 管理前端、合同包和 VitePress 文档，使用 Conventional Commits；`openspec/config.yaml` 固定为 `spec-driven`。Python 后端位于 `apps/backend`，使用 Python >=3.10、`uv`、`hatchling` 和 `src` layout，唯一导入根为 `super_ai`，禁止 `src.super_ai`。

后端最小运行时为 FastAPI 与 Pydantic v2；持久化基线锁定 SQLAlchemy 2 async、aiosqlite 与 Alembic，但 foundation 不创建连接或迁移。测试与质量基线为 pytest、pytest-asyncio（`asyncio_mode=auto`）、Ruff（line-length 100、target py310、B/E/F/I/UP）和 strict Pyright。

后续 Agent/AI 提案必须使用 LangChain 1.x `create_agent`、LangGraph、`langchain-openai`、`langchain-mcp-adapters`、MCP、pymilvus 3、rank-bm25、pypdf、`langchain-text-splitters` 与 httpx 的边界；foundation 不安装或调用真实服务。前端锁定 Vue 3.5、Vite 6、TypeScript 5.6 strict（`exactOptionalPropertyTypes`、`noUncheckedIndexedAccess`、`isolatedModules`、ES2022/Bundler resolution）、Pinia 3、Vue Router 4、Vitest 2、marked、DOMPurify 和 lucide-vue-next。

选择两套包管理器而非强行统一：Python 的可复现解析、虚拟环境和构建元数据由 uv 负责，JS workspace 图由 npm 负责；各自锁文件是唯一真相。

### 后端应用工厂与导入安全

`super_ai.app:create_app` 创建 FastAPI 实例并注册 `/health`。配置加载和未来依赖通过显式函数/依赖注入进入应用工厂，而不是模块全局初始化。测试在导入后 monkeypatch 连接入口，断言没有 SQLite、Milvus、LLM 或 MCP 连接发生。

替代方案是模块级单例或启动时自动连接；拒绝它们，因为会使类型检查、测试与命令行导入依赖本机服务，且会扩大机密暴露面。

### 本地 JSON 配置与公开面

仅提交 `config/project.template.json` 和 `config/user.project.template.json`，每个 key、secret、password 值均为空。`project_config.py` 读取同目录的 `project.json`，在存在时递归深合并 `user.project.json`；它不读取任何 OS 环境变量。不存在的用户覆盖文件视为可选，缺少必需项目文件时报清晰错误。P06 才增加 LLM 的类型验证与 provider。

前端的 Vite 配置在构建时使用同一深合并语义读取本地配置，但只经 `define` 注入一份公开对象到 `src/config.ts`：`frontend.title`、`frontend.apiBaseUrl` 与 `frontend.analytics.publicKey`。禁止源代码直接导入完整 JSON；哨兵机密测试检查 `dist`。

替代方案是把 JSON 导入前端或使用环境变量；拒绝前者，因为静态打包会泄露未使用机密，拒绝后者，因为项目配置必须可审计地只来自本地 JSON。

### 运行与基础设施边界

`infra/README.md` 只记录最终 Compose 服务：etcd、MinIO、Milvus、Attu、Alertmanager。后端、前端、官方 CLS MCP Server 在主机运行。目录只放说明和保留位，不放 Compose 定义或应用镜像。

### 测试策略与安装顺序

实现首先写入针对目录、脚本、忽略规则、Python 导入安全、深合并与前端公开 allowlist 的最小测试。生成 `package.json` 和 `pyproject.toml` 后，先执行根 `npm install`，再执行后端 `uv sync`；临时配置由测试创建，开发者真实配置不参与测试。最终门禁顺序为 OpenSpec 验证、后端 Ruff/Pyright/pytest、合同 typecheck/test、前端 typecheck/test/build、`git diff --check`。

## Risks / Trade-offs

- [前端构建需要本地配置] → 构建脚本从模板创建被忽略的空配置，并且测试用临时目录配置。
- [将来依赖清单较大] → 在项目指南锁定边界但仅在需要该能力的后续提案中增加 Agent/AI 运行依赖。
- [JSON 未提供静态模式校验] → foundation 只承担通用加载；P06 按约定引入 LLM 的类型验证与 provider。
- [主机运行使本地服务编排不统一] → 通过清晰运行位置和禁止应用 Compose 服务避免边界漂移。

## Migration Plan

1. 初始化 Git 并建立忽略规则与模板，确保本机配置不可暂存。
2. 创建工作区骨架、项目指南与只含边界说明的基础设施、文档。
3. 安装 npm 和 uv 依赖，执行测试及质量门禁。
4. 若新建骨架失败，删除未跟踪的工作区文件或重新从空仓库创建；不会修改远程历史或执行 force push。
