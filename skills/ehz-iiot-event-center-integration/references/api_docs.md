# 极联事件中心集成 API 文档

## 一、接口配置

| 配置项 | 说明 | 环境变量 |
|--------|------|---------|
| API 地址 | 极联产品后端地址 | API_URL |
| API Key | 认证密钥 | API_KEY |
| Token | Bearer 认证 Token | API_TOKEN |

## 二、通用请求头

```
Authorization: Bearer {token}
Sys-Apikey: {apikey}
Content-Type: application/json
```

## 三、API 类型说明

本技能接口根据前缀分为两类，请求参数和返回值格式不同：

### 类型一：/ESBREST/iiot/ 前缀接口

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

### 类型二：/ESBREST/faas/ 前缀接口

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

## 四、接口清单

### 1. 事件中心申明表-分页列表查询

**接口地址**: `GET /ESBREST/iiot/event/EventDefine/list`
**接口类型**: iiot
**作用**: 分页查询事件中心申明记录列表

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
| createTime | string | 否 | 创建日期，精确匹配事件创建时间，格式为 `YYYY-MM-DD HH:mm:ss` | |
| updateBy | string | 否 | 更新人，精确匹配执行最近一次更新操作的用户名 | |
| updateTime | string | 否 | 更新日期，精确匹配事件最近更新时间，格式为 `YYYY-MM-DD HH:mm:ss` | |
| condJson | array | 否 | 指标条件（JSON 格式），数组元素包含 `eid`、`condition`、`field`、`text`、`value`、`relation` 字段 |
| condJson[].eid | string | 否 | 设备/实体 ID，条件关联的设备或实体标识 | |
| condJson[].condition | string | 否 | 比较运算符，如 `>`、`<`、`=`、`!=` 等 | |
| condJson[].field | string | 否 | 字段名，条件所针对的数据字段名称 | |
| condJson[].text | string | 否 | 展示文本，条件的可视化描述文本 | |
| condJson[].value | string | 否 | 比较值，条件判断的阈值或目标值 | |
| condJson[].relation | string | 否 | 逻辑关系，当前仅支持 `"and"`，表示与其他条件以 AND 逻辑组合 | |
| dataFormatJson | array | 否 | 数据格式（JSON 格式），数组元素为 `{code, name, describe, type}` 对象 |
| dataFormatJson[].code | string | 否 | 字段编码，数据格式中该字段的唯一标识 | |
| dataFormatJson[].name | string | 否 | 字段名称，数据格式中该字段的展示名称 | |
| dataFormatJson[].describe | string | 否 | 字段描述，数据格式中该字段的详细说明 | |
| dataFormatJson[].type | string | 否 | 字段类型，如 `"string"`、`"integer"`、`"boolean"` 等 | |

**入参示例**:

```string
pageNo=1&pageSize=10
```

**返回字段说明**:

| 字段名 | 类型 | 说明 |
|-------|------|------|
| success | boolean | 成功标志，`true` 表示请求成功，`false` 表示失败 |
| code | integer | 返回代码，`200` 表示成功，其他值表示异常或错误 |
| message | string | 返回处理消息，成功时通常为空字符串，失败时返回具体错误信息 |
| result | Object | 返回数据对象，包含 `records` 列表及分页元信息 |
| result.records | array | 数据记录列表，数组中每个元素为一条事件中心申明记录 |
| result.records[].id | string | 主键 ID，事件中心申明的唯一标识 |
| result.records[].name | string | 名称，事件中心的名称描述 |
| result.records[].type | string | 事件类型，如 `"system"` 表示基于系统事件， `"cond` 表示基于指标条件, `"cron`" 表示基于定时器事件  |
| result.records[].topic | string | 主题，事件所属的主题/Topic 标识 |
| result.records[].cron | string | Cron 表达式，定义事件的触发时间规则，格式为标准 6 位 Cron（秒 分 时 日 月 周）|
| result.records[].cond | string | 指标条件，JSON 字符串格式的条件数组，描述事件触发的前置条件 |
| result.records[].condJson | array | 指标条件（JSON 解析后），数组元素包含 `eid`、`condition`、`field`、`text`、`value`、`relation` 字段 |
| result.records[].condJson[].eid | string | 设备/实体 ID，条件关联的设备或实体标识 |
| result.records[].condJson[].condition | string | 比较运算符，如 `>`、`<`、`=`、`!=` 等 |
| result.records[].condJson[].field | string | 字段名，条件所针对的数据字段名称 |
| result.records[].condJson[].text | string | 展示文本，条件的可视化描述文本 |
| result.records[].condJson[].value | string | 比较值，条件判断的阈值或目标值 |
| result.records[].condJson[].relation | string | 逻辑关系，当前仅支持 `"and"`，表示与其他条件以 AND 逻辑组合 |
| result.records[].description | string | 描述，事件中心的文字说明 |
| result.records[].dataFormat | string | 数据格式，JSON 字符串格式，定义事件携带的数据字段结构 |
| result.records[].dataFormatJson | array | 数据格式（JSON 解析后），数组元素为 `{code, name, describe, type}` 对象 |
| result.records[].dataFormatJson[].code | string | 字段编码，数据格式中该字段的唯一标识 |
| result.records[].dataFormatJson[].name | string | 字段名称，数据格式中该字段的展示名称 |
| result.records[].dataFormatJson[].describe | string | 字段描述，数据格式中该字段的详细说明 |
| result.records[].dataFormatJson[].type | string | 字段类型，当前为 `"string"`，表示字符串类型 |
| result.records[].status | string | 状态，`"0"` 表示关闭（禁用），`"1"` 表示启用 |
| result.records[].jobId | integer | 定时任务 ID，关联后端定时任务系统的任务标识，`0` 或 `null` 表示未关联 |
| result.records[].createBy | string | 创建人，执行新增操作的用户名 |
| result.records[].createTime | string | 创建日期，格式为 `YYYY-MM-DD HH:mm:ss` |
| result.records[].updateBy | string | 更新人，执行最近一次更新操作的用户名 |
| result.records[].updateTime | string | 更新日期，格式为 `YYYY-MM-DD HH:mm:ss` |
| result.total | integer | 符合条件的总记录数，用于分页计算 |
| result.size | integer | 每页显示的记录条数，对应请求参数 `pageSize` |
| result.current | integer | 当前页码，对应请求参数 `pageNo` |
| result.orders | array | 排序信息列表，通常为空数组，表示无自定义排序 |
| result.optimizeCountSql | boolean | 是否优化 Count SQL 查询，`true` 表示启用了优化 |
| result.searchCount | boolean | 是否计算总数，`true` 表示返回的 `total` 值为精确统计 |
| result.countId | string / null | Count 查询使用的字段标识，通常为 `null` |
| result.maxLimit | string / null | 最大返回条数限制，`null` 表示无限制 |
| result.pages | integer | 总页数，根据 `total` 和 `size` 计算得出 |
| timestamp | integer | 响应时间戳（毫秒），从 Unix epoch (1970-01-01 00:00:00 UTC) 至今的毫秒数 |
| requestId | string | 请求唯一标识 UUID，用于追踪和日志关联 |

**返回示例**:

```json
{
  "success": true,
  "message": "",
  "code": 200,
  "result": {
    "records": [{
      "id": "2019323421428367361",
      "name": "测试事件中心功能",
      "type": "cron",
      "topic": "TEST-MASTER-IOT-yhtest",
      "cron": "0 * * * * ? *",
      "cond": "[{\"eid\":\"\",\"condition\":\"\",\"field\":\"\",\"text\":\"\",\"value\":\"\",\"relation\":\"and\"}]",
      "condJson": [{
        "eid": "",
        "condition": "",
        "field": "",
        "text": "",
        "value": "",
        "relation": "and"
      }],
      "description": "测试事件中心功能",
      "dataFormat": "[{\"code\":\"time\",\"name\":\"时间表达式\",\"describe\":\"这是一个Cron表达式\",\"type\":\"string\"}]",
      "dataFormatJson": [{
        "code": "time",
        "name": "时间表达式",
        "describe": "这是一个Cron表达式",
        "type": "string"
      }],
      "status": "0",
      "jobId": 244,
      "createBy": "admin",
      "createTime": "2026-02-05 16:13:16",
      "updateBy": "admin",
      "updateTime": "2026-03-20 15:00:13"
    }],
    "total": 9,
    "size": 10,
    "current": 1,
    "orders": [],
    "optimizeCountSql": true,
    "searchCount": true,
    "countId": null,
    "maxLimit": null,
    "pages": 1
  },
  "timestamp": 1775100747758,
  "requestId": "8a49912c9d4c390f019d4c3fdfee0026"
}
```

---

### 2. 事件中心动作表-分页列表查询

**接口地址**: `GET /ESBREST/iiot/event/eventAction/list`
**接口类型**: iiot
**作用**: 分页查询事件中心动作记录列表

**请求参数**:

| 参数 | 类型 | 必填 | 说明                                                                                                                                | 默认值 |
|------|------|------|-----------------------------------------------------------------------------------------------------------------------------------|--------|
| pageNo | integer | 否 | 页码，请求第几页数据，从 1 开始                                                                                                                 | 1 |
| pageSize | integer | 否 | 每页记录数，限制单次返回的数据条数                                                                                                                 | 10 |
| keyword | string | 否 | 关键字，用于模糊匹配动作名称、别名等字段进行搜索过滤                                                                                                        | |
| id | string | 否 | 主键 ID，精确匹配动作记录的唯一标识                                                                                                               | |
| actionAlias | string | 否 | 动作别名，精确匹配动作的简短标识名称                                                                                                                | |
| actionName | string | 否 | 动作名称，精确匹配动作的展示名称                                                                                                                  | |
| actionType | string | 否 | 动作类型，精确匹配动作的执行方式，如 `"kafka`" 表示 转发到kafka; `"rabbitmq`" 表示 转发到rabbitmq;  `"set`" 表示 指标设置; `"service`" 表示 服务调用;  `"script"` 表示 规则脚本 | |
| actionStatus | string | 否 | 动作状态，精确匹配动作启用状态：`"0"` 表示关闭，`"1"` 表示启用                                                                                             | |
| defineName | string | 否 | 事件名称，精确匹配关联的事件中心申明的名称                                                                                                             | |
| defineTopic | string | 否 | 事件主题，精确匹配关联的事件中心申明的 Topic 标识                                                                                                      | |
| eventAction | string | 否 | 事件动作，JSON 字符串格式的动作配置，描述如何执行该动作                                                                                                    | |
| createBy | string | 否 | 创建人，精确匹配执行新增操作的用户名                                                                                                                | |
| createTime | string | 否 | 创建日期，精确匹配动作创建时间，格式为 `YYYY-MM-DD HH:mm:ss`                                                                                         | |
| updateBy | string | 否 | 更新人，精确匹配执行最近一次更新操作的用户名                                                                                                            | |
| updateTime | string | 否 | 更新日期，精确匹配动作最近更新时间，格式为 `YYYY-MM-DD HH:mm:ss`                                                                                       | |

**入参示例**:

```string
pageNo=1&pageSize=10&keyword=TEST-TOPIC-1775119483-39e9a588&actionType=script&actionStatus=
```

**返回字段说明**:

| 字段名 | 类型 | 说明 |
|-------|------|------|
| success | boolean | 成功标志，`true` 表示请求成功，`false` 表示失败 |
| code | integer | 返回代码，`200` 表示成功，其他值表示异常或错误 |
| message | string | 返回处理消息，成功时通常为空字符串，失败时返回具体错误信息 |
| result | Object | 返回数据对象，包含 `records` 列表及分页元信息 |
| result.records | array | 数据记录列表，数组中每个元素为一条事件中心动作记录 |
| result.records[].id | string | 主键 ID，动作记录的唯一标识 |
| result.records[].actionAlias | string | 动作别名，动作的简短标识名称 |
| result.records[].actionName | string | 动作名称，动作的展示名称 |
| result.records[].actionType | string | 动作类型，当前为 `"http"` 表示 HTTP 请求动作 |
| result.records[].actionStatus | string | 动作状态，`"0"` 表示关闭（禁用），`"1"` 表示启用 |
| result.records[].defineName | string | 事件名称，关联的事件中心申明的名称 |
| result.records[].defineTopic | string | 事件主题，关联的事件中心申明的 Topic 标识 |
| result.records[].eventAction | string | 事件动作，JSON 字符串格式的动作配置，描述如何执行该动作 |
| result.records[].eventActionJson | Object | 事件动作（JSON 解析后），包含 `url` 和 `method` 等字段 |
| result.records[].eventActionJson.url | string | 请求 URL，动作执行时发送 HTTP 请求的目标地址 |
| result.records[].eventActionJson.method | string | 请求方法，当前为 `"POST"`，支持 `GET`、`POST`、`PUT`、`DELETE` 等 |
| result.records[].createBy | string | 创建人，执行新增操作的用户名 |
| result.records[].createTime | string | 创建日期，格式为 `YYYY-MM-DD HH:mm:ss` |
| result.records[].updateBy | string | 更新人，执行最近一次更新操作的用户名 |
| result.records[].updateTime | string | 更新日期，格式为 `YYYY-MM-DD HH:mm:ss` |
| result.total | integer | 符合条件的总记录数，用于分页计算 |
| result.size | integer | 每页显示的记录条数，对应请求参数 `pageSize` |
| result.current | integer | 当前页码，对应请求参数 `pageNo` |
| result.pages | integer | 总页数，根据 `total` 和 `size` 计算得出 |
| timestamp | integer | 响应时间戳（毫秒），从 Unix epoch (1970-01-01 00:00:00 UTC) 至今的毫秒数 |
| requestId | string | 请求唯一标识 UUID，用于追踪和日志关联 |

**返回示例**:

```json
{
  "success": true,
  "code": 200,
  "message": "",
  "result": {
    "records": [{
      "id": "2039582630135476226",
      "actionAlias": "测试动作别名",
      "actionName": "测试动作名称",
      "actionType": "http",
      "actionStatus": "1",
      "defineName": "测试事件中心功能",
      "defineTopic": "TEST-MASTER-IOT-yhtest",
      "eventAction": "{\"url\":\"https://example.com/webhook\",\"method\":\"POST\"}",
      "eventActionJson": {
        "url": "https://example.com/webhook",
        "method": "POST"
      },
      "createBy": "admin",
      "createTime": "2026-02-05 16:13:16",
      "updateBy": "admin",
      "updateTime": "2026-03-20 15:00:13"
    }],
    "total": 1,
    "size": 10,
    "current": 1,
    "pages": 1
  },
  "timestamp": 1775100747758,
  "requestId": "8a49912c9d4c390f019d4c3fdfee0026"
}
```

---

### 3. 事件中心申明表-分页列表查询-导出专用

**接口地址**: `GET /ESBREST/iiot/event/EventDefine/listAll`
**接口类型**: iiot
**作用**: 导出所有事件中心申明记录（不分页，返回完整数据集）

**请求参数**:

| 参数 | 类型 | 必填 | 说明                                                                        | 默认值 |
|------|------|------|---------------------------------------------------------------------------|--------|
| keyword | string | 否 | 关键字，用于模糊匹配名称、描述等字段进行搜索过滤                                                  | |
| name | string | 否 | 名称，精确匹配事件中心申明的名称                                                          | |
| type | string | 否 | 类型，事件类型，如 `"system"` 表示基于系统事件， `"cond` 表示基于指标条件, `"cron`" 表示基于定时器事件       | |
| topic | string | 否 | 主题，精确匹配事件所属的主题/Topic 标识                                                   | |
| cron | string | 否 | Cron 表达式，模糊匹配事件的触发时间规则                                                    | |
| status | string | 否 | 状态，精确匹配事件启用状态：`"0"` 表示关闭，`"1"` 表示启用                                       | |
| id | string | 否 | 主键 ID，精确匹配事件中心申明的唯一标识                                                     | |
| description | string | 否 | 描述，模糊匹配事件中心的文字说明                                                          | |
| jobId | integer | 否 | 定时任务 ID，精确匹配关联的后端定时任务标识                                                   | |
| createBy | string | 否 | 创建人，精确匹配执行新增操作的用户名                                                        | |
| createTime | string | 否 | 创建日期，精确匹配事件创建时间，格式为 `YYYY-MM-DD HH:mm:ss`                                 | |
| updateBy | string | 否 | 更新人，精确匹配执行最近一次更新操作的用户名                                                    | |
| updateTime | string | 否 | 更新日期，精确匹配事件最近更新时间，格式为 `YYYY-MM-DD HH:mm:ss`                               | |
| condJson | array | 否 | 指标条件（JSON 格式），数组元素包含 `eid`、`condition`、`field`、`text`、`value`、`relation` 字段 |
| condJson[].eid | string | 否 | 设备/实体 ID，条件关联的设备或实体标识                                                     | |
| condJson[].condition | string | 否 | 比较运算符，如 `>`、`<`、`=`、`!=` 等                                                | |
| condJson[].field | string | 否 | 字段名，条件所针对的数据字段名称                                                          | |
| condJson[].text | string | 否 | 展示文本，条件的可视化描述文本                                                           | |
| condJson[].value | string | 否 | 比较值，条件判断的阈值或目标值                                                           | |
| condJson[].relation | string | 否 | 逻辑关系，当前仅支持 `"and"`，表示与其他条件以 AND 逻辑组合                                      | |
| dataFormatJson | array | 否 | 数据格式（JSON 格式），数组元素为 `{code, name, describe, type}` 对象                     |
| dataFormatJson[].code | string | 否 | 字段编码，数据格式中该字段的唯一标识                                                        | |
| dataFormatJson[].name | string | 否 | 字段名称，数据格式中该字段的展示名称                                                        | |
| dataFormatJson[].describe | string | 否 | 字段描述，数据格式中该字段的详细说明                                                        | |
| dataFormatJson[].type | string | 否 | 字段类型，如 `"string"`、`"integer"`、`"boolean"` 等                               | |

**入参示例**:

```string
name=测试事件&status=1
```

**返回字段说明**:

| 字段名 | 类型 | 说明 |
|-------|------|------|
| success | boolean | 成功标志，`true` 表示请求成功，`false` 表示失败 |
| code | integer | 返回代码，`200` 表示成功，其他值表示异常或错误 |
| message | string | 返回处理消息，成功时通常为空字符串，失败时返回具体错误信息 |
| result | Object | 返回数据对象，包含 `records` 列表 |
| result.records | array | 数据记录列表，数组中每个元素为一条事件中心申明记录（结构同接口1） |
| result.total | integer | 符合条件的总记录数 |
| result.size | integer | 每页显示的记录条数 |
| result.current | integer | 当前页码 |
| result.pages | integer | 总页数 |
| timestamp | integer | 响应时间戳（毫秒），从 Unix epoch 至今的毫秒数 |
| requestId | string | 请求唯一标识 UUID，用于追踪和日志关联 |

**返回示例**:

```json
{
  "success": true,
  "code": 200,
  "message": "",
  "result": {
    "records": [{
      "id": "2019323421428367361",
      "name": "测试事件中心功能",
      "type": "cron",
      "topic": "TEST-MASTER-IOT-yhtest",
      "cron": "0 * * * * ? *",
      "cond": "[{\"eid\":\"\",\"condition\":\"\",\"field\":\"\",\"text\":\"\",\"value\":\"\",\"relation\":\"and\"}]",
      "condJson": [{
        "eid": "",
        "condition": "",
        "field": "",
        "text": "",
        "value": "",
        "relation": "and"
      }],
      "description": "测试事件中心功能",
      "dataFormat": "[{\"code\":\"time\",\"name\":\"时间表达式\",\"describe\":\"这是一个Cron表达式\",\"type\":\"string\"}]",
      "dataFormatJson": [{
        "code": "time",
        "name": "时间表达式",
        "describe": "这是一个Cron表达式",
        "type": "string"
      }],
      "status": "0",
      "jobId": 244,
      "createBy": "admin",
      "createTime": "2026-02-05 16:13:16",
      "updateBy": "admin",
      "updateTime": "2026-03-20 15:00:13"
    }],
    "total": 9,
    "size": 10,
    "current": 1,
    "pages": 1
  },
  "timestamp": 1775100747758,
  "requestId": "8a49912c9d4c390f019d4c3fdfee0026"
}
```

---

### 4. 事件中心动作表-发布事件消息到指定队列类型

**接口地址**: `POST /ESBREST/faas/coode/sendToEventMessage`
**接口类型**: faas
**作用**: 发布事件消息到指定队列类型，支持 kafka、rabbitmq、mqtt 队列

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| topic | string | 是 | 发送消息的主题/Topic，用于指定消息发送到哪个主题 | |
| type | string | 是 | 队列类型，指定消息队列的类型枚举值，支持：`kafka`、`rabbitmq`、`mqtt` | |
| msgs | Object | 是 | 发送的消息内容，JSON 对象格式，包含需要传递的业务数据字段 | |

**入参示例**:

```json
{
  "msgs": {
    "name": "test1",
    "value": 123
  },
  "topic": "test-topic",
  "type": "kafka"
}
```

**返回字段说明**:

| 字段名 | 类型 | 说明 |
|-------|------|------|
| errorCode | integer | 错误代码，`0` 表示成功，其他值表示失败 |
| errorMsg | string | 错误信息，成功时返回消息发送的描述信息，失败时返回具体错误原因 |
| return | Object | 返回数据对象，发布操作成功时为空的 `{}` 对象 |

**返回示例**:

```json
{
  "errorCode": 0,
  "errorMsg": "发布事件消息sendToEventMessage:消息类型【kafka】【主题test-topic】内容【{'name': 'test1', 'value': 123}】",
  "return": {}
}
```

---

## 五、通用说明

### 错误码说明

#### iiot 类型错误码

| 错误码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 认证失败 |
| 404 | 资源不存在 |
| 408 | 请求超时 |
| 500 | 服务器内部错误 |
| 502 | 网关错误 |
| 503 | 服务不可用 |

#### faas 类型错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 400 | 请求参数错误 |
| 401 | 认证失败 |
| 404 | 命令未找到 |
| 408 | 请求超时 |
| 500 | 服务器内部错误 |

### 错误响应格式

#### iiot 类型错误响应

```json
{
  "success": false,
  "message": "错误描述",
  "code": 500,
  "result": null,
  "timestamp": 1775025131933,
  "requestId": "8a49804a9d454a98019d47be119d16cf"
}
```

#### faas 类型错误响应

```json
{
  "errorCode": 400,
  "errorMsg": "参数错误",
  "return": null
}
```

---

## 六、快速参考

| 操作 | 接口类型 | 命令 |
|------|---------|------|
| 事件中心申明列表 | iiot | `GET /ESBREST/iiot/event/EventDefine/list` |
| 事件中心动作列表 | iiot | `GET /ESBREST/iiot/event/eventAction/list` |
| 导出事件中心申明 | iiot | `GET /ESBREST/iiot/event/EventDefine/listAll` |
| 发布事件消息 | faas | `POST /ESBREST/faas/coode/sendToEventMessage` |
