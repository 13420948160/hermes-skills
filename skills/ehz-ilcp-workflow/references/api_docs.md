# ehz-ilcp-workflow管理 API 文档

## 接口配置

| 配置项 | 说明 | 环境变量 |
|--------|------|---------|
| API 地址 | 极联产品后端地址 | API_URL |
| API Key | 认证密钥 | API_KEY |
| Token | Bearer 认证 Token | API_TOEKN |

## 通用请求头

```
Authorization: Bearer {token}
Sys-Apikey: {apikey}
Content-Type: application/json
```

## 通用请求参数

```
{"apikey": "{apikey}", "request": {request}}
```


## 接口清单

### 1. 发起审批流

**接口地址**: `POST /ESBREST/faas/code/initiateFlow`
**作用**: 发起一个新的审批流程实例

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|-------|------|------|------|------|
| flowid | String | 是 | 审批流程定义ID | |
| initiator | String | 是 | 发起人用户ID | |
| formFields | Object | 是 | 表单字段数据对象 | {"datas": []} |
| formFields.datas | Array | 是 | 表单字段数组 | |
| formFields.datas[].field | String | 是 | 字段标识 | |
| formFields.datas[].value | String | 是 | 字段值 | |
| bid | String | 否 | 业务ID，不传则自动生成UUID | 空 |
| suggestion | String | 否 | 审批意见/说明 | 空 |


**请求示例**: 

```json
{
  "flowid": "FLOW_001",
  "initiator": "user001",
  "formFields": {
    "datas": [
      {"field": "applyReason", "value": "申请采购物料"},
      {"field": "amount", "value": 10000}
    ]
  },
  "bid": "BIZ20260327001",
  "suggestion": "请领导审批"
}
```

**返回字段说明**: 

| 字段名 | 类型 | 说明 |
|-------|------|------|
| errorCode | Number | 错误码，0表示成功 |
| errorMsg | String | 错误消息 |
| return | Object | 返回数据 |
| return.bid | String | 流程实例ID |

**返回示例**: 

```json
{
  "errorCode": 0,
  "errorMsg": "success",
  "return": {
    "bid": "BIZ20260327001"
  }
}
```

### 2. 获取审批流实例状态

**接口地址**: `POST /ESBREST/faas/code/getFlowState`
**作用**: 根据实例ID获取工作流实例的当前状态

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|-------|------|------|------|------|
| bid | String | 是 | 流程实例ID | |

**请求示例**: 

```json
{
  "bid": "BIZ20260327001"
}
```

**返回字段说明**: 

| 字段名 | 类型 | 说明 |
|-------|------|------|
| errorCode | Number | 错误码，0表示成功 |
| errorMsg | String | 错误消息 |
| return | Object | 流程实例信息 |
| return.flowid | String | 流程定义ID |
| return.flowGroup | String | 流程分组名称 |
| return.initiator | String | 发起人用户ID |
| return.initiatorName | String | 发起人姓名 |
| return.initiateTime | String | 发起时间 |
| return.lastProcessTime | String | 最后处理时间 |
| return.currentProcessor | Array | 当前处理人列表 |
| return.currentState | Number | 当前状态(0:处理中,1:已撤销,2:已完成) |
| return.formState | Array | 表单字段状态 |
| return.formState[].field | String | 字段标识 |
| return.formState[].value | String | 字段值 |

**返回示例**: 

```json
{
  "errorCode": 0,
  "errorMsg": "success",
  "return": {
    "flowid": "FLOW_001",
    "flowGroup": "采购审批",
    "initiator": "user001",
    "initiatorName": "张三",
    "initiateTime": "2026-03-27 10:00:00",
    "lastProcessTime": "2026-03-27 14:30:00",
    "currentProcessor": ["user002", "user003"],
    "currentState": 0,
    "formState": [
      {"field": "applyReason", "value": "申请采购物料"},
      {"field": "amount", "value": 10000}
    ]
  }
}
```

### 3. 撤销审批流

**接口地址**: `POST /ESBREST/faas/code/repealFlow`
**作用**: 撤销当前用户发起的审批流实例（只能撤销自己发起的、处理中的流程）

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|-------|------|------|------|------|
| bid | String | 是 | 流程实例ID | |
| suggestion | String | 否 | 撤销原因/说明 | 空 |


**请求示例**:

```json
{
  "bid": "BIZ20260327001",
  "suggestion": "申请有误，需要重新提交"
}
```

**返回字段说明**:

| 字段名 | 类型 | 说明 |
|-------|------|------|
| errorCode | Number | 错误码，0表示成功 |
| errorMsg | String | 错误消息 |
| return | Object | 撤销后的流程实例信息 |
| return.flowid | String | 流程定义ID |
| return.version | Number | 流程版本号 |
| return.bid | String | 流程实例ID |
| return.flowGroup | String | 流程分组名称 |
| return.initiator | String | 发起人用户ID |
| return.initiatorName | String | 发起人姓名 |
| return.initiateTime | String | 发起时间 |
| return.lastProcessTime | String | 最后处理时间 |
| return.currentProcessor | Array | 当前处理人列表 |
| return.currentState | Number | 当前状态(0:处理中,1:已撤销,2:已完成) |
| return.formState | Array | 表单字段状态 |
| return.formState[].field | String | 字段标识/字段名 |
| return.formState[].value | String/Number | 字段值 |

**返回示例**:

```json
{
  "errorCode": 0,
  "errorMsg": "success",
  "return": {
    "flowid": "FLOW_001",
    "flowGroup": "采购审批",
    "initiator": "user001",
    "initiatorName": "张三",
    "initiateTime": "2026-03-27 10:00:00",
    "lastProcessTime": "2026-03-27 15:00:00",
    "currentProcessor": [],
    "currentState": 1,
    "formState": [
      {"field": "applyReason", "value": "申请采购物料"},
      {"field": "amount", "value": 10000}
    ]
  }
}
```

**错误码**:

| 错误码 | 说明 |
|--------|------|
| -1000 | 用户权限不足，无权处理 |

### 4. 获取审批流完成记录

**接口地址**: `POST /ESBREST/faas/code/getFlowFinishRecord`
**作用**: 查询指定发起人在指定时间范围内完成的所有审批流记录

**请求参数**:

| 参数名 | 类型 | 必填 | 说明 | 默认值 |
|-------|------|------|------|------|
| initiator | String | 是 | 发起人用户ID | |
| startTime | String | 是 | 查询开始时间，格式：YYYY-MM-DD HH:mm:ss | |
| endTime | String | 是 | 查询结束时间，格式：YYYY-MM-DD HH:mm:ss | |


**请求示例**:

```json
{
  "initiator": "user001",
  "startTime": "2026-03-01 00:00:00",
  "endTime": "2026-03-31 23:59:59"
}
```

**返回字段说明**:

| 字段名 | 类型 | 说明 |
|-------|------|------|
| errorCode | Number | 错误码，0表示成功 |
| errorMsg | String | 错误消息 |
| return | Object | 返回数据 |
| return.record | Array | 完成记录列表 |
| return.record[].flowid | String | 流程定义ID |
| return.record[].version | Number | 流程版本号 |
| return.record[].bid | String | 流程实例ID |
| return.record[].flowGroup | String | 流程分组名称 |
| return.record[].initiator | String | 发起人用户ID |
| return.record[].initiatorName | String | 发起人姓名 |
| return.record[].initiateTime | String | 发起时间 |
| return.record[].finishTime | String | 完成时间 |
| return.record[].formState | Array | 表单字段最终状态 |
| return.record[].formState[].field | String | 字段标识/字段名 |
| return.record[].formState[].value | String/Number | 字段值 |

**返回示例**:

```json
{
  "errorCode": 0,
  "errorMsg": "success",
  "return": {
    "record": [
      {
        "flowid": "FLOW_001",
        "version": 1,
        "bid": "BIZ20260327001",
        "flowGroup": "采购审批",
        "initiator": "user001",
        "initiatorName": "张三",
        "initiateTime": "2026-03-27 10:00:00",
        "finishTime": "2026-03-27 14:30:00",
        "formState": [
          {"field": "applyReason", "value": "申请采购物料"},
          {"field": "amount", "value": 10000}
        ]
      }
    ]
  }
}
```

---

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 400 | 请求参数错误 |
| 401 | 认证失败 |
| 404 | 审批流不存在 |
| 408 | 请求超时 |
| 500 | 服务器内部错误 |
| 502 | 网关错误 |
| 503 | 服务不可用 |

---
