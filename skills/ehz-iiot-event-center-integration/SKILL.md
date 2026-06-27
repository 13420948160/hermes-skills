---
name: ehz-iiot-event-center-integration
description: 极联平台事件中心集成 API 技能，支持事件中心申明管理（列表）和动作管理（列表/消息发布）。
version: "1.0.0"
author: "ehz"
license: MIT
metadata:
  hermes:
    tags: [iiot, event, center, integration]
    related_skills: []
---

# ehz-iiot-event-center-integration 技能使用说明

封装极联平台事件中心集成 API，支持事件中心申明管理和动作管理功能。

## 一、环境配置

### 1.1 复制环境变量模板

```bash
cd skills/ehz-iiot-event-center-integration
cp .env.example .env
```

### 1.2 编辑 `.env` 文件，填入实际值

| 变量名 | 说明 | 示例 |
|--------|------|------|
| API_URL | API 服务器地址 | https://jilian-sit.ehzcloud.com |
| ACCOUNT_ID | 极联平台账号 | admin |
| SECRET_ID | 密钥ID | hziot |
| SECRET_KEY | 密钥KEY | your_secret_key_here |
| TOKEN_VALID_SECONDS | Token 有效期（秒） | 900 |

> **提示**：如不创建 `.env` 文件，程序会自动读取系统环境变量，等效于已 export 所有变量。

**认证说明**：`TOKEN` 无需手动配置，客户端启动时会自动调用 `/ESBREST/faas/code/getAccessToken` 接口换取，token 有效期 15 分钟，客户端会自动刷新。

---

## 二、API 类型说明

本技能接口根据前缀分为两类，请求参数和返回值格式不同：

### 类型一：/ESBREST/iiot/ 前缀接口（iiot 类型）

请求方式：GET（参数放 URL query string）或 POST（参数放 JSON body）
请求参数：直接 JSON 对象
返回值格式：
```json
{
  "success": true,
  "message": "操作成功",
  "code": 200,
  "result": { ... },
  "timestamp": 1775025131933,
  "requestId": "8a49804a9d454a98019d47be119d16cf"
}
```

### 类型二：/ESBREST/faas/ 前缀接口（faas 类型）

请求方式：POST
请求参数：必须包装在 `{ apikey: "", request: { ... } }` 结构中
返回值格式：
```json
{
  "errorCode": 0,
  "errorMsg": "操作成功",
  "times": "mySql总耗时 -> 0.123 秒。Redis总耗时 -> 0.005 秒。",
  "return": { ... }
}
```

---

## 三、接口清单

| # | 接口类型 | 方法 | 接口地址 | 说明 |
|---|---------|------|---------|------|
| 1 | iiot | GET | `/ESBREST/iiot/event/EventDefine/list` | 事件中心申明表-分页列表查询 |
| 2 | iiot | GET | `/ESBREST/iiot/event/eventAction/list` | 事件中心动作表-分页列表查询 |
| 3 | iiot | GET | `/ESBREST/iiot/event/EventDefine/listAll` | 事件中心申明表-导出专用（不分页） |
| 4 | faas | POST | `/ESBREST/faas/coode/sendToEventMessage` | 发布事件消息到指定队列类型 |

---

## 四、查询命令

### 4.1 查看所有可用命令

```bash
cd skills/ehz-iiot-event-center-integration
python scripts/client.py --help
```

### 4.2 事件中心申明表-分页列表查询（iiot）

```bash
# 默认（第一页，每页10条）
python scripts/client.py event-define-list

# 关键字搜索
python scripts/client.py event-define-list --keyword 测试

# 按状态筛选（0=关闭，1=启用）
python scripts/client.py event-define-list --status 1

# 按类型筛选
python scripts/client.py event-define-list --type cron

# 自定义分页
python scripts/client.py event-define-list --page-no 1 --page-size 20
```

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| pageNo | integer | 否 | 页码，请求第几页数据，从 1 开始 | 1 |
| pageSize | integer | 否 | 每页记录数，限制单次返回的数据条数 | 10 |
| keyword | string | 否 | 关键字，用于模糊匹配名称、描述等字段进行搜索过滤 | |
| name | string | 否 | 名称，精确匹配事件中心申明的名称 | |
| type | string | 否 | 类型，事件类型，如 `"cron"` 表示基于 Cron 表达式的定时事件 | |
| topic | string | 否 | 主题，精确匹配事件所属的主题/Topic 标识 | |
| cron | string | 否 | Cron 表达式，模糊匹配事件的触发时间规则 | |
| status | string | 否 | 状态，精确匹配事件启用状态：`"0"` 表示关闭，`"1"` 表示启用 | |
| id | string | 否 | 主键 ID，精确匹配事件中心申明的唯一标识 | |
| description | string | 否 | 描述，模糊匹配事件中心的文字说明 | |
| jobId | integer | 否 | 定时任务 ID，精确匹配关联的后端定时任务标识 | |
| createBy | string | 否 | 创建人，精确匹配执行新增操作的用户名 | |
| createTime | string | 否 | 创建日期，精确匹配事件创建时间 | |
| updateBy | string | 否 | 更新人，精确匹配执行最近一次更新操作的用户名 | |
| updateTime | string | 否 | 更新日期，精确匹配事件最近更新时间 | |

**返回字段**: `success`, `code`, `message`, `result.records[]`, `result.total`, `result.pages`

---

### 4.3 事件中心动作表-分页列表查询（iiot）

```bash
# 默认（第一页，每页10条）
python scripts/client.py event-action-list

# 按动作名称搜索
python scripts/client.py event-action-list --action-name 测试

# 按动作类型筛选（有效值：kafka / rabbitmq / set / service / script）
python scripts/client.py event-action-list --action-type kafka

# 按状态筛选（0=关闭，1=启用）
python scripts/client.py event-action-list --action-status 1

# 自定义分页
python scripts/client.py event-action-list --page-no 1 --page-size 20
```

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| pageNo | integer | 否 | 页码，请求第几页数据，从 1 开始 | 1 |
| pageSize | integer | 否 | 每页记录数，限制单次返回的数据条数 | 10 |
| keyword | string | 否 | 关键字，用于模糊匹配动作名称、别名等字段进行搜索过滤 | |
| id | string | 否 | 主键 ID，精确匹配动作记录的唯一标识 | |
| actionAlias | string | 否 | 动作别名，精确匹配动作的简短标识名称 | |
| actionName | string | 否 | 动作名称，精确匹配动作的展示名称 | |
| actionType | string | 否 | 动作类型，枚举值：`kafka`=转发kafka；`rabbitmq`=转发rabbitmq；`set`=指标设置；`service`=服务调用；`script`=规则脚本 | |
| actionStatus | string | 否 | 动作状态，精确匹配动作启用状态：`"0"` 表示关闭，`"1"` 表示启用 | |
| defineName | string | 否 | 事件名称，精确匹配关联的事件中心申明的名称 | |
| defineTopic | string | 否 | 事件主题，精确匹配关联的事件中心申明的 Topic 标识 | |
| eventAction | string | 否 | 事件动作，JSON 字符串格式的动作配置，描述如何执行该动作 | |
| createBy | string | 否 | 创建人，精确匹配执行新增操作的用户名 | |
| createTime | string | 否 | 创建日期，精确匹配动作创建时间 | |
| updateBy | string | 否 | 更新人，精确匹配执行最近一次更新操作的用户名 | |
| updateTime | string | 否 | 更新日期，精确匹配动作最近更新时间 | |

**返回字段**: `success`, `code`, `message`, `result.records[]`, `result.total`, `result.pages`

---

### 4.4 事件中心申明表-导出专用（iiot）

```bash
# 导出所有记录
python scripts/client.py event-define-export-all

# 按名称筛选导出
python scripts/client.py event-define-export-all --name 测试

# 按状态筛选导出
python scripts/client.py event-define-export-all --status 1
```

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| keyword | string | 否 | 关键字，用于模糊匹配名称、描述等字段进行搜索过滤 | |
| name | string | 否 | 名称，精确匹配事件中心申明的名称 | |
| type | string | 否 | 类型，事件类型，如 `"cron"` 表示基于 Cron 表达式的定时事件 | |
| topic | string | 否 | 主题，精确匹配事件所属的主题/Topic 标识 | |
| cron | string | 否 | Cron 表达式，模糊匹配事件的触发时间规则 | |
| status | string | 否 | 状态，精确匹配事件启用状态：`"0"` 表示关闭，`"1"` 表示启用 | |
| id | string | 否 | 主键 ID，精确匹配事件中心申明的唯一标识 | |
| description | string | 否 | 描述，模糊匹配事件中心的文字说明 | |
| jobId | integer | 否 | 定时任务 ID，精确匹配关联的后端定时任务标识 | |
| createBy | string | 否 | 创建人，精确匹配执行新增操作的用户名 | |
| createTime | string | 否 | 创建日期，精确匹配事件创建时间 | |
| updateBy | string | 否 | 更新人，精确匹配执行最近一次更新操作的用户名 | |
| updateTime | string | 否 | 更新日期，精确匹配事件最近更新时间 | |

**返回字段**: `success`, `code`, `message`, `result.records[]`

---

### 4.5 事件中心动作表-发布事件消息到指定队列类型（faas）

```bash
# 发布 kafka 消息
python scripts/client.py send-to-event-message \
  --topic test-topic \
  --type kafka \
  --msgs '{"name": "test1", "value": 123}'

# 发布 rabbitmq 消息
python scripts/client.py send-to-event-message \
  --topic test-topic \
  --type rabbitmq \
  --msgs '{"name": "test2"}'

# 发布 mqtt 消息
python scripts/client.py send-to-event-message \
  --topic test-topic \
  --type mqtt \
  --msgs '{"name": "test3"}'
```

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| topic | string | 是 | 发送消息的主题/Topic，用于指定消息发送到哪个主题 | |
| type | string | 是 | 队列类型，指定消息队列的类型枚举值，支持：`kafka`、`rabbitmq`、`mqtt` | |
| msgs | Object | 是 | 发送的消息内容，JSON 对象格式，包含需要传递的业务数据字段 | |

**返回字段**: `errorCode`, `errorMsg`, `return`

---

## 五、返回格式

### iiot 类型成功

```json
{
  "success": true,
  "message": "",
  "code": 200,
  "result": { ... },
  "timestamp": 1774935858801,
  "requestId": "8a4981749d408f08019d426bde711737"
}
```

### faas 类型成功

```json
{
  "errorCode": 0,
  "errorMsg": "操作成功",
  "times": "mySql总耗时 -> 0.123 秒。Redis总耗时 -> 0.005 秒。",
  "return": { ... }
}
```

### iiot 类型错误

```json
{
  "success": false,
  "message": "错误描述",
  "code": 500
}
```

### faas 类型错误

```json
{
  "errorCode": 400,
  "errorMsg": "参数错误",
  "return": null
}
```

---

## 六、常见错误码排查

| 错误码 | 类型 | 说明 | 排查方法 |
|--------|------|------|---------|
| 401 | 通用 | 认证失败 | 检查 SECRET_ID / SECRET_KEY 是否正确 |
| 408 | 通用 | 请求超时 | 检查网络连通性或 API_URL 是否正确 |
| 502 | 通用 | 响应非 JSON | 服务器异常，检查 API 服务状态 |
| 503 | 通用 | 无法连接服务器 | 检查 API_URL 是否可达 |
| 200 | iiot | 成功 | - |
| 0 | faas | 成功 | - |
| 500 | 通用 | 未知错误 | 查看错误信息详情，必要时开启 DEBUG 日志 |

---

## 七、测试

```bash
cd skills/ehz-iiot-event-center-integration
# 运行所有测试
python scripts/test_client.py

# 输出报告到文件（文本 + JSON）
python scripts/test_client.py -o test_report.txt 2>&1

# 运行指定测试（支持模糊匹配）
python scripts/test_client.py event_define_list

# 列出所有测试用例
python scripts/test_client.py --list

# 查看帮助
python scripts/test_client.py --help
```

**测试策略**：
- 每个接口原子化独立测试，互不影响
- 同一用例最多 15 次重试，连续 15 次失败直接退出
- 测试报告包含：执行结果、通过率、失败率

---

## 八、快速参考

| 操作 | 命令 |
|------|------|
| 查看帮助 | `python scripts/client.py --help` |
| 事件中心申明列表 | `python scripts/client.py event-define-list` |
| 事件中心动作列表 | `python scripts/client.py event-action-list` |
| 导出所有事件中心申明 | `python scripts/client.py event-define-export-all` |
| 发布事件消息 | `python scripts/client.py send-to-event-message --topic <主题> --type <kafka/rabbitmq/mqtt> --msgs <JSON>` |
| 运行测试 | `python scripts/test_client.py` |
