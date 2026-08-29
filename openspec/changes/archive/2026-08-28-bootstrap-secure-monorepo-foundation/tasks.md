## 1. 仓库与项目治理

- [x] 1.1 初始化 Git、根忽略规则、npm workspaces、OpenSpec 项目上下文和中文根 README，并通过目录与 ignore 测试验证基础边界。
- [x] 1.2 编写根 AGENTS.md、各工作区 README、VitePress 与基础设施说明，并通过文本边界测试确认不宣称未实现功能或应用 Compose 服务。

## 2. 安全配置基础

- [x] 2.1 创建无值的项目与用户配置模板及通用递归深合并实现，并通过临时配置测试验证合并、不读取环境变量和本机配置被忽略。
- [x] 2.2 创建前端构建期公开配置 allowlist 与哨兵构建扫描，并通过测试证明机密不会出现在 `dist`。

## 3. 后端工作区

- [x] 3.1 创建 Python src layout、uv/hatchling 元数据及 Ruff、Pyright、pytest 配置，并在生成 pyproject 后执行 `uv sync` 验证依赖环境。
- [x] 3.2 以测试先行实现 `super_ai` 应用工厂和 `/health`，并通过 pytest、Ruff 和 strict Pyright 验证顶级导入与导入安全。

## 4. 前端与合同工作区

- [x] 4.1 创建严格 TypeScript 的 API 合同入口、测试和 npm scripts，并通过 contracts typecheck/test 验证最小 foundation 类型。
- [x] 4.2 创建 Vue/Vite 桌面 Web 骨架、路由、状态、Vitest 和脚本，并在生成 package.json 后执行根 `npm install` 及 frontend typecheck/test/build 验证。

## 5. 端到端质量门禁

- [x] 5.1 执行 `openspec validate --all`、后端 Ruff/Pyright/pytest、contracts typecheck/test、frontend typecheck/test/build 与 `git diff --check`，修复所有发现的问题并记录结果。
