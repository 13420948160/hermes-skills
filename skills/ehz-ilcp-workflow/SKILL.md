---
name: ehz-ilcp-workflow
description: ILCP 审批流技能，支持发起审批流、查询审批状态、撤销审批、获取完成记录。
license: MIT
metadata:
  author: "ehz"
  version: "1.0.0"
---

# ehz-ilcp-workflow 技能使用说明

封装 ILCP 审批流 API，支持发起审批流、查询审批状态、撤销审批、获取完成记录。

## 一、环境配置

### 1.1 复制环境变量模板

```bash
cd skills/ehz-ilcp-workflow
cp .env.example .env
```

### 1.2 编辑 `.env` 文件，填入实际值

| 变量名 | 说明 | 示例 |
|--------|------|------|
| API_URL | API 服务器地址 | your_api_url_here |
| ACCOUNT_ID | 用户ID（AccountId） | your_account_id_here |
| SECRET_ID | 密钥ID | your_secret_id_here |
| SECRET_KEY | 密钥KEY | your_secret_key_here |
| TOKEN_VALID_SECONDS | Token 有效期（秒） | 900 |

> **提示**：如不创建 `.env` 文件，程序会自动读取系统环境变量，等效于已 export 所有变量。

**认证说明**：`TOKEN` 无需手动配置，客户端启动时会自动调用 `/ESBREST/faas/code/getAccessToken` 接口换取，token 有效期 15 分钟，客户端会自动刷新。

---

## 二、查询命令

### 2.1 查看所有可用命令

```bash
cd skills/ehz-ilcp-workflow
python scripts/client.py --help
```

### 2.2 发起审批流

发起一个新的审批流程实例。

```bash
# 最小参数（必填）
python scripts/client.py initiate-flow --flowid FLOW_001 --initiator user001

# 带业务ID和审批意见
python scripts/client.py initiate-flow --flowid FLOW_001 --initiator user001 --bid BIZ20260327001 --suggestion 请领导审批

# 带表单字段（JSON 字符串）
python scripts/client.py initiate-flow --flowid FLOW_001 --initiator user001 --formFields "{\"datas\":[{\"field\":\"applyReason\",\"value\":\"申请采购物料\"},{\"field\":\"amount\",\"value\":10000}]}"

# 带表单字段（默认值，自动生成bid）
python scripts/client.py initiate-flow --flowid FLOW_001 --initiator user001 --formFields "{\"datas\":[{\"field\":\"applyReason\",\"value\":\"测试\"}]}"
```

### 2.3 获取审批流实例状态

根据实例ID获取工作流实例的当前状态。

```bash
# 基本用法
python scripts/client.py get-flow-state --bid BIZ20260327001

# 也可用中文命令名
python scripts/client.py 获取审批流实例状态 --bid BIZ20260327001
```

### 2.4 撤销审批流

撤销当前用户发起的审批流实例（只能撤销自己发起的、处理中的流程）。

```bash
# 基本撤销
python scripts/client.py repeal-flow --bid BIZ20260327001

# 带撤销原因
python scripts/client.py repeal-flow --bid BIZ20260327001 --suggestion 申请有误，需要重新提交

# 也可用中文命令名
python scripts/client.py 撤销审批流 --bid BIZ20260327001
```

### 2.5 获取审批流完成记录

查询指定发起人在指定时间范围内的所有已完结审批流记录。

```bash
# 按发起人和时间范围查询
python scripts/client.py get-finish-record --initiator user001 --startTime "2026-03-01 00:00:00" --endTime "2026-03-31 23:59:59"

# 查询当月记录
python scripts/client.py get-finish-record --initiator user001 --startTime "2026-03-01 00:00:00" --endTime "2026-03-31 23:59:59"
```

### 调用流程

1. 配置环境变量（见上方）
2. 执行对应命令
3. 客户端自动调用 `/ESBREST/faas/code/getAccessToken` 获取 token（有效期 `TOKEN_VALID_SECONDS` 秒，过期自动刷新）
4. 返回 JSON 格式结果

### 返回格式

成功：
```json
{
  "errorCode": 0,
  "errorMsg": "success",
  "return": { ... }
}
```

失败：
```json
{
  "errorCode": 401,
  "errorMsg": "认证失败：...",
  "return": null
}
```

---

## 三、查看特定命令的详细帮助

```bash
# 发起审批流帮助
python scripts/client.py initiate-flow --help

# 查询状态帮助
python scripts/client.py get-flow-state --help

# 撤销审批帮助
python scripts/client.py repeal-flow --help

# 完成记录帮助
python scripts/client.py get-finish-record --help
```

---

## 四、日志与调试

### 4.1 开启调试日志

默认日志级别为 INFO，如需查看请求详情，在 `scripts/client.py` 中修改：

```python
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(message)s")
```

### 4.2 常见错误码排查

| 错误码 | 说明 | 排查方法 |
|--------|------|---------|
| 0 | 成功 | - |
| 400 | 请求参数错误 | 检查必填参数是否完整，参数类型是否正确 |
| 401 | 认证失败 | 检查 SECRET_ID / SECRET_KEY 是否正确，凭证是否过期 |
| 404 | 审批流不存在 | 检查 bid 是否正确，流程实例是否存在 |
| -1000 | 用户权限不足 | 检查当前账号是否有权操作该审批流 |
| 408 | 请求超时 | 检查网络连通性或 API_URL 是否正确 |
| 500 | 服务器内部错误 | 查看 errorMsg 详情，必要时开启 DEBUG 日志 |
| 502 | 网关错误 | 服务器异常，检查 API 服务状态 |
| 503 | 服务不可用 | 检查 API 服务是否正常运行 |

---

## 五、SKILL.md 文档生成

当 `references/api_docs.md` 更新后，需重新生成 `SKILL.md`：

```bash
cd skills/ehz-ilcp-workflow
python scripts/generate_skill.py
```

指定自定义路径（不常用）：

```bash
python scripts/generate_skill.py \
  --api-docs references/api_docs.md \
  --output SKILL.md \
  --skill-name ehz-ilcp-workflow
```

---

## 六、代码热更新流程（开发者）

当平台新增 API 接口时，只需：

1. **更新文档**：`references/api_docs.md` 按格式新增接口章节
2
2. **验证命令**：`python scripts/client.py --help` → 新命令自动出现

无需修改任何 Python 代码。

---

## 七、快速参考

| 操作 | 命令 |
|------|------|
| 查看帮助 | `python scripts/client.py --help` |
| 发起审批流 | `python scripts/client.py initiate-flow --flowid <ID> --initiator <用户ID>` |
| 查询审批状态 | `python scripts/client.py get-flow-state --bid <实例ID>` |
| 撤销审批流 | `python scripts/client.py repeal-flow --bid <实例ID> --suggestion <原因>` |
| 查询完成记录 | `python scripts/client.py get-finish-record --initiator <用户ID> --startTime <开始> --endTime <结束>` |
| 命令详细帮助 | `python scripts/client.py <命令名> --help` |
