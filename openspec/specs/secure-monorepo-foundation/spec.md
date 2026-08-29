# secure-monorepo-foundation Specification

## Purpose

为后续产品提案提供一个可在本地稳定构建、验证并保护配置机密的单体仓库基础，明确应用、合同、文档和基础设施的责任边界。

## Requirements

### Requirement: 工作区提供可发现的基础目录与质量入口
仓库 SHALL 提供后端、前端、API 合同、配置、基础设施、脚本、OpenSpec 和文档目录，并为前端、合同和文档暴露可从根工作区调用的构建或验证入口。

#### Scenario: 开发者检查仓库骨架
- **WHEN** 开发者在新检出的仓库中查看根目录和根工作区脚本
- **THEN** 可以发现每个基础目录及前端、合同和文档的明确入口，且说明文档只描述已经存在的骨架与验证方式

### Requirement: 后端健康服务可导入且不产生外部连接
后端 SHALL 提供一个返回健康状态的 HTTP 服务工厂；任何后端模块在导入期间 MUST NOT 连接 SQLite、Milvus、LLM 或 MCP，并且包内导入 MUST 使用顶级应用包名。

#### Scenario: 导入后端应用
- **WHEN** 测试进程在未配置真实外部服务的环境中导入后端应用并调用健康端点
- **THEN** 导入不产生网络或数据库连接，且端点返回成功状态与健康载荷

### Requirement: 本地项目配置执行安全深合并
应用 SHALL 以提交的无密钥模板为起点，从本地项目 JSON 读取配置，并以用户项目 JSON 递归深合并覆盖；应用 MUST NOT 使用操作系统环境变量作为项目配置来源。

#### Scenario: 用户覆盖嵌套配置
- **WHEN** 项目配置和用户配置包含同一嵌套对象的不同字段
- **THEN** 合并结果保留未覆盖字段并仅覆盖用户指定字段

#### Scenario: 本地机密不进入版本控制
- **WHEN** 开发者从模板创建本机项目配置并检查 Git 忽略规则
- **THEN** 本机配置、环境文件、构建产物、缓存、数据库和日志均不会成为可提交文件

### Requirement: 浏览器只接收明确公开的配置字段
前端 SHALL 仅接收标题、API 基地址和明确标记为公开的分析键等 allowlist 配置；所有 LLM、CLS、MCP、MinIO 及其他机密字段 MUST NOT 被打包到浏览器产物中。

#### Scenario: 使用哨兵机密构建前端
- **WHEN** 构建配置含有唯一的哨兵机密值
- **THEN** 构建产物中不存在该哨兵值，且前端仍可读取允许公开的配置字段

### Requirement: 基础设施职责与应用运行位置明确分离
基础设施说明 SHALL 将 Compose 的最终职责限定为 etcd、MinIO、Milvus、Attu 和 Alertmanager，并明确后端、前端和官方 CLS MCP Server MUST 在主机运行；基础骨架 MUST NOT 创建应用镜像、项目 Compose 文件或应用 Compose 服务。

#### Scenario: 审查基础设施目录
- **WHEN** 维护者查看基础设施目录与项目指南
- **THEN** 能确认允许的 Compose 服务边界，并且找不到应用 Dockerfile、项目 Compose 文件或应用服务定义

### Requirement: 基线质量门禁可独立执行
仓库 SHALL 提供后端静态检查、类型检查和测试，以及合同和前端的类型检查、测试与构建；测试 MUST 使用临时配置而非开发者真实本机配置。

#### Scenario: 在干净工作区运行门禁
- **WHEN** 开发者先安装声明的依赖并执行项目质量命令
- **THEN** 每个命令可以在不读取真实凭据或启动外部服务的条件下完成
