# Hermes Skills Hub 管理指南

## 概述

Hermes 技能（Skills）是可复用的工作流程和规范，以 Markdown 文档形式存储，支持从 GitHub 仓库发布和安装。

## 核心概念

| | 技能 (Skills) | 插件 (Plugins) |
|---|---|---|
| 定位 | 可复用的事件处理流程和操作规范 | 系统功能扩展 |
| 存放位置 | `~/.hermes/skills/` | `~/.hermes/plugins/` |
| 内容形式 | Markdown + YAML frontmatter | Python 代码 |
| 用途 | 工作流、排查步骤、最佳实践 | 扩展工具能力 |
| 加载方式 | 运行时按需加载 | 启动时全局加载 |
| 管理命令 | `hermes skills *` | `hermes plugins *` |

**一句话总结：技能 = Agent 的"经验知识库"；插件 = Agent 的"工具箱"**

## 目录结构

```
skills/
└── <category>/
    └── <skill-name>/
        └── SKILL.md           # 必需：技能定义
        └── references/        # 可选：附加文档
        └── scripts/           # 可选：辅助脚本
        └── templates/         # 可选：文件模板
```

## SKILL.md 格式规范

文件必须以 `---` 开头，包含以下 frontmatter：

```markdown
---
name: skill-name                # 小写，hyphen分隔，≤64字符
description: Use when <触发条件>. <一句话行为描述>.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [tag1, tag2]
    related_skills: [other-skill]
---

# 技能标题

## Overview
说明做什么、为什么。

## When to Use
- 触发条件1
- 触发条件2

## 正文内容
具体步骤、最佳实践、命令示例等。

## Common Pitfalls
1. 常见错误及修复

## Verification Checklist
- [ ] 验证项1
- [ ] 验证项2
```

### 关键约束

- `description` ≤ 1024 字符
- 文件必须以 `---` 开头（无前导空白）
- 总文件大小 ≤ 100,000 字符
- `name` 字段全局唯一

## 自建 Skills Hub

### 方式一：GitHub 仓库（推荐）

**1. 接入 Hub（tap add）**

```bash
hermes skills tap add owner/repo
```

> 注意：`tap add` 仅支持 GitHub，不支持 GitLab

**2. 推送技能到 GitHub**

```bash
git clone https://github.com/owner/repo.git
# 创建技能文件
git add -A && git commit -m "feat: add <skill-name>"
git push origin main
```

**3. 安装技能**

```bash
# 从 repo 安装（需要先 tap add）
hermes skills install owner/repo/skills/category/skill-name

# 强制重装（已安装时使用）
hermes skills install owner/repo/skills/category/skill-name --force

# 从 raw URL 直接安装（无需 tap）
hermes skills install "https://raw.githubusercontent.com/owner/repo/main/skills/category/skill-name/SKILL.md" --name skill-name
```

### 方式二：手动安装

```bash
mkdir -p ~/.hermes/skills/<category>/<skill-name>
# 下载或复制 SKILL.md 到该目录
cp SKILL.md ~/.hermes/skills/<category>/<skill-name>/
```

### 方式三：GitLab（有限支持）

GitLab 仓库不能使用 `tap add`，但可以通过 URL 安装：

```bash
# 需要获取 GitLab raw 文件的直接 URL
hermes skills install "<gitlab-raw-url>" --name skill-name
```

## 常用命令

| 命令 | 说明 |
|------|------|
| `hermes skills list` | 列出所有已安装技能 |
| `hermes skills search <query>` | 搜索技能 |
| `hermes skills browse` | 浏览 Hub 上所有可用技能 |
| `hermes skills tap list` | 查看已配置的 taps |
| `hermes skills tap add owner/repo` | 添加 GitHub 仓库为技能源 |
| `hermes skills tap remove owner/repo` | 移除技能源 |
| `hermes skills install <identifier>` | 安装技能 |
| `hermes skills install <url>` | 从 URL 安装技能 |
| `hermes skills inspect <identifier>` | 预览技能内容 |
| `hermes skills uninstall <name>` | 卸载技能 |
| `/skill <name>` | 在会话中加载技能 |

## GITHUB_TOKEN 配置

`hermes skills install` 需要 GitHub API 认证才能正常使用。推荐配置方式：

### 1. 获取 Token

- 创建 **Classic token**（经典 PAT，`ghp_` 开头）：https://github.com/settings/tokens/new
- 权限选择：`Contents: Read`（仅读取仓库内容）
- 注意：**Fine-grained PAT**（`github_pat_` 开头）可能导致 Git Trees API 认证失败，推荐用经典 PAT

### 2. 写入配置文件

```bash
echo "GITHUB_TOKEN=ghp_your_token_here" >> ~/.hermes/.env
```

### 3. 安装前清理环境

当前 shell 会话可能继承了旧 token，安装前清除：

```bash
unset GITHUB_TOKEN
source ~/.hermes/.env
hermes skills install owner/repo/skills/category/skill-name
```

## 搜索不到刚上传的技能？

`hermes skills search` 搜不到但 `hermes skills install` 可以正常安装，常见原因：

### 1. 目录层级过深（最常见）

`hermes skills search` 只扫描 tap 路径下的一级子目录。如果你的技能放在 `skills/category/skill-name`（两层），search 只能看到 `category` 级别，不会递归进入查找。

**解决：** 安装时用完整路径即可，search 搜不到不影响使用：

```bash
hermes skills install owner/repo/skills/category/skill-name
```

要支持 search，需将技能目录改为单层结构：

```bash
skills/skill-name/SKILL.md           # ✅ 能被 search 搜到
skills/category/skill-name/SKILL.md  # ❌ 搜不到，但可以 install
```

### 2. Tap 索引缓存延迟

新添加的 tap 需要一段时间才能被索引缓存。索引刷新后即可搜索。

---

**总结：直接 `hermes skills install` 安装即可，search 搜不到是正常现象，不影响使用。**

## 默认 Taps

Hermes 默认包含以下官方 taps：

| Repo | 说明 |
|------|------|
| `openai/skills` | OpenAI 精选技能 |
| `anthropics/skills` | Anthropic 技能 |
| `huggingface/skills` | HuggingFace 技能 |
| `NVIDIA/skills` | NVIDIA 官方技能 |

## 验证清单

新建技能后，确认以下事项：

- [ ] SKILL.md 文件以 `---` 开头（无前导空白）
- [ ] frontmatter 包含 `name`、`description`、`version`、`author`、`license`、`metadata`
- [ ] `description` 字段 ≤ 1024 字符
- [ ] 技能目录结构正确
- [ ] 已推送到 GitHub
- [ ] `hermes skills install` 安装成功
- [ ] `/skill <name>` 加载无报错