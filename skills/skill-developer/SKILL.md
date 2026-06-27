---
name: skill-developer
description: Interactive skill development assistant. Invoke when user wants to create, design, or develop a new skill through conversation. Guides user through skill creation with templates and best practices.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [skill, create, develop, template, assistant]
    related_skills: []
  skill_developer:
    default_output_dir: /Users/tangjun/mycode/hermes-skills/skills
---

# Skill Developer Assistant

## 概述

通过对话方式引导用户创建和开发新的 Hermes Skill。提供交互式体验，自动生成符合规范的 SKILL.md 文件和目录结构。

## 使用场景

- 用户想要创建一个新的 skill
- 用户需要帮助设计 skill 结构
- 用户希望通过对话方式开发 skill
- 用户需要 skill 开发的最佳实践指导

## 工作流程

### 1. 需求收集阶段

通过对话收集以下信息：

1. **Skill 基本信息**
   - Skill 名称（唯一标识符）
   - 简短描述（≤ 200 字符）
   - 版本号（默认 1.0.0）
   - 作者信息

2. **Skill 功能定义**
   - 主要功能是什么？
   - 解决什么问题？
   - 适用的使用场景？

3. **技术实现**
   - 是否需要脚本文件？（scripts/）
   - 是否需要参考文档？（references/）
   - 是否需要模板文件？（templates/）
   - 是否需要环境变量？（.env.example）

### 2. 内容生成阶段

根据收集的信息，自动生成：

1. **SKILL.md 文件**
   - 包含完整的 frontmatter
   - 结构化的文档内容
   - 使用说明和示例

2. **目录结构**（可选）
   ```
   <skill-name>/
   ├── SKILL.md           # 必需：技能定义文件
   ├── scripts/           # 可选：脚本文件
   │   └── *.py
   ├── references/        # 可选：参考文档
   │   └── *.md
   ├── templates/        # 可选：模板文件
   └── .env.example      # 可选：环境变量示例
   ```

3. **README.md**（可选）
   - 详细的使用说明
   - 安装步骤
   - 配置指南

### 3. 验证和输出阶段

1. **验证规则检查**
   - 描述长度 ≤ 200 字符
   - frontmatter 格式正确
   - 文件从第一行开始（无前导空白）

2. **保存文件**
   - 默认保存到：`/Users/tangjun/mycode/hermes-skills/skills/<skill-name>/`
   - 用户可指定其他路径

3. **提供下一步指导**
   - 如何测试新 skill
   - 如何安装到 Trae
   - 如何推送到 Git 仓库

## 交互式问题模板

### 问题 1：Skill 基础信息
```
请告诉我你想创建的 skill 的基本信息：
- Skill 名称（建议使用 kebab-case，如 my-awesome-skill）
- 一句话描述（≤ 200 字符）
- 版本号（默认 1.0.0）
- 作者名称
```

### 问题 2：功能定位
```
这个 skill 的主要功能是什么？
- 它解决了什么问题？
- 用户在什么情况下会使用它？
- 它需要执行什么操作？
```

### 问题 3：技术实现
```
这个 skill 需要哪些技术组件？
□ Python 脚本（scripts/*.py）
□ API 客户端（scripts/client.py）
□ 参考文档（references/*.md）
□ 模板文件（templates/*）
□ 环境变量配置（.env.example）
□ 测试文件（tests/*.py）
```

### 问题 4：文档完善
```
需要生成哪些文档？
□ 详细的使用指南
□ API 文档
□ 配置说明
□ 示例代码
```

## Skill 模板示例

### 最小化 Skill

```markdown
---
name: my-skill
description: Brief description of what this skill does and when to invoke it.
---

# My Skill

## 概述
简要描述 skill 的功能和使用场景。

## 使用方式
说明如何使用这个 skill。
```

### 完整 Skill

```markdown
---
name: api-integration
description: Integrates with XYZ API for data operations. Invoke when user needs to query or update data from XYZ service.
version: 1.0.0
author: Your Name
license: MIT
metadata:
  hermes:
    tags: [api, integration, data]
    related_skills: []
---

# API Integration Skill

## 概述
提供与 XYZ API 的集成能力，支持数据查询、更新和删除操作。

## 环境配置
创建 `.env` 文件并配置以下变量...

## 使用方式
```bash
python scripts/client.py --help
```

## API 功能
- 查询数据
- 更新记录
- 删除记录
```

## 最佳实践

### 1. 描述字段规范

**好的示例：**
```
description: "Integrates with XYZ API for data operations. Invoke when user needs to query or update data from XYZ service."
```

**不好的示例：**
```
description: "A skill that does something"  # 太模糊，没有说明何时使用
```

### 2. 文件结构组织

- **SKILL.md**：必需文件，包含 skill 定义和使用说明
- **scripts/**：存放可执行脚本
- **references/**：存放 API 文档、技术文档
- **templates/**：存放代码模板、配置模板
- **tests/**：存放测试文件

### 3. 命名规范

- Skill 名称：使用 `kebab-case`（如 `data-processor`）
- 脚本文件：使用 `snake_case`（如 `data_processor.py`）
- 文档文件：使用 `snake_case.md`

### 4. 版本管理

遵循语义化版本：
- MAJOR：不兼容的 API 变更
- MINOR：向后兼容的功能新增
- PATCH：向后兼容的问题修复

## 开发流程指导

### 步骤 1：规划 Skill
1. 明确 skill 的目标和用途
2. 确定需要的功能组件
3. 规划文件结构

### 步骤 2：创建文件
1. 创建 skill 目录
2. 编写 SKILL.md 文件
3. 实现脚本功能
4. 编写文档

### 步骤 3：测试验证
1. 本地测试脚本功能
2. 验证 skill 结构
3. 测试 skill 加载

### 步骤 4：发布部署
1. 提交到 Git 仓库
2. 推送到 Hermes Skills Hub
3. 安装到 Trae

## 常见问题

### Q1: 描述字段应该多长？
A: 建议 ≤ 200 字符，确保在列表中完整显示。必须包含：(1) 功能说明 (2) 触发条件。

### Q2: 是否需要 README.md？
A: 如果 skill 较复杂，建议添加 README.md 提供详细说明。简单 skill 可省略。

### Q3: 如何处理敏感信息？
A: 使用 `.env.example` 提供模板，实际值存放在 `.env` 文件中（不提交到 Git）。

### Q4: Skill 如何调试？
A: 1) 先在本地测试脚本 2) 使用 `python scripts/client.py` 测试功能 3) 加载 skill 验证格式。

## 输出位置

默认保存路径：`/Users/tangjun/mycode/hermes-skills/skills/<skill-name>/`

用户可在对话中指定其他路径。

## 验证检查清单

创建 skill 后，检查以下项：

- [ ] SKILL.md 文件存在
- [ ] frontmatter 格式正确（包含 name, description, version, author, license）
- [ ] description ≤ 200 字符
- [ ] 文件以 `---` 开头（无前导空白）
- [ ] 必需的目录已创建
- [ ] 脚本文件可执行
- [ ] 文档完整清晰

## 开始创建

当用户表示要创建新 skill 时，按照以下流程：

1. 问候并说明将引导创建过程
2. 使用上述问题模板收集信息
3. 根据回答生成 skill 结构
4. 创建文件并保存到指定位置
5. 提供测试和安装指导
6. 询问是否需要进一步调整

---

**示例对话：**

```
用户：我想创建一个 skill 来处理数据分析
助手：太好了！我将帮助你创建一个数据分析 skill。让我们开始：

首先，请告诉我：
1. Skill 名称（建议使用 kebab-case，如 data-analyzer）
2. 一句话描述（≤ 200 字符）
3. 作者名称

用户：名称是 data-analyzer，描述是"分析数据并生成报告。当用户需要处理数据文件或生成分析报告时使用"，作者是张三

助手：很好！现在让我了解这个 skill 的功能...

[继续收集信息并生成 skill]
```