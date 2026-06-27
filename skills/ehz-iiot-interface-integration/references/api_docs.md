# 极联平台 API 文档

## 接口配置

| 配置项    | 说明         | 环境变量     |
|---------|------------|-----------|
| API 地址 | 极联产品后端地址 | API_URL   |
| API Key | 认证密钥       | API_KEY   |
| Token   | Bearer 认证 Token | API_TOKEN |

## 通用请求头

```
Authorization: Bearer {token}
Sys-Apikey: {apikey}
Content-Type: application/json
```

## 接口清单

| #  | 接口地址                                    | 作用                           |
|----|-----------------------------------------|------------------------------|
| 1  | `POST /ESBREST/edge/app/getAppList`       | 获取API管理应用接入列表               |
| 2  | `POST /ESBREST/edge/app/getAppInterfaceList` | 根据标识符查询接口服务列表              |
| 3  | `POST /ESBREST/faas/code/get_interface_doc` | 获取单个接口文档                    |
| 4  | `POST /ESBREST/edge/app/debugAppInterface` | 调用API管理接口服务                 |

---

## 1. 获取API管理应用接入列表

**接口地址**: `POST /ESBREST/edge/app/getAppList`
**作用**: API管理-获取API管理应用接入列表
**备注**: 接口的【应用基础参数列表】参数返回值是动态, 由字段 connect【连接器-协议标识】决定

### 请求参数

| 字段路径    | 类型      | 必填 | 说明                                 |
|-----------|---------|----|------------------------------------|
| name      | string  | 否  | 查找关键字，用于模糊匹配应用名称进行搜索过滤         |
| page      | integer | 是  | 当前第几页，从 1 开始                    |
| size      | integer | 是  | 每页多少条数据                          |

**入参示例**:

```json
{
  "page": 1,
  "size": 10,
  "name": ""
}
```

### 返回字段

| 字段路径                          | 类型      | 必填 | 说明                                                                 |
|---------------------------------|---------|----|--------------------------------------------------------------------|
| errorCode                       | integer | 是  | 错误码，0=成功，非 0=失败                                                    |
| errorMsg                        | string  | 是  | 错误信息，成功时为"执行成功！"                                                   |
| return                          | Object  | 否  | 返回数据对象，失败时为 null                                                   |
| return.list[]                   | array   | 是  | 应用接入记录列表                                                           |
| return.list[].id                | integer | 是  | 应用记录主键 ID                                                          |
| return.list[].appId             | string  | 是  | 应用唯一标识符（UUID 格式），用于关联接口服务                                          |
| return.list[].page              | integer | 是  | 分页页码（当前固定为 0，无实际分页意义）                                              |
| return.list[].size              | integer | 是  | 分页大小（当前固定为 0，无实际分页意义）                                              |
| return.list[].code              | string  | 是  | 应用代码/标识，如"faasbusi"标识业务云函数管理                                       |
| return.list[].name              | string  | 是  | 应用名称，展示用，如"业务云函数管理"                                                |
| return.list[].state            | integer | 是  | 应用状态，1=启用，0=停用                                                     |
| return.list[].connect          | string  | 是  | 连接协议标识，格式如"EHZAPPV1.0.0.1"                                         |
| return.list[].describe         | string  | 是  | 应用描述说明                                                             |
| return.list[].qty              | integer | 是  | 该应用下注册的接口服务数量                                                      |
| return.list[].baseParam[]      | array   | 是  | 应用基础参数列表（包含接入凭证等信息） 该参数下一级返回值是动态变化的，由字段 connect【连接器-协议标识】决定                               |
| return.list[].baseParam[].id    | string  | 是  | 参数标识，枚举值：`url`=服务地址；`addr`=接口地址；`token`=认证令牌；`apikey`=API密钥        |
| return.list[].baseParam[].name | string  | 是  | 参数名称，如"服务地址"、"接口地址"、"token"、"apikey"                               |
| return.list[].baseParam[].type | string  | 是  | 参数类型，固定为"3"（表示加密字符串类型）                                             |
| return.list[].baseParam[].value | string | 是  | 参数值，`url`填写网关地址；`addr`填写接口代理路径；`token`填写JWT令牌；`apikey`填写Base64编码凭证 |
| return.total                   | integer | 是  | 满足查询条件的应用接入记录总条数                                                   |
| result                          | null    | 是  | 兼容字段，固定为 null                                                      |
| code                            | integer | 是  | 兼容错误码，同 errorCode                                                  |
| msg                             | null    | 是  | 兼容字段，固定为 null                                                      |
| message                         | null    | 是  | 兼容字段，固定为 null                                                      |

**返回示例**:

```json
{
  "errorCode": 0,
  "errorMsg": "执行成功！",
  "return": {
    "list": [{
      "id": 128,
      "appId": "3710e1d4-7a76-40d0-84a5-81224d3fe892",
      "page": 0,
      "size": 0,
      "code": "faasbusi",
      "name": "业务云函数管理",
      "state": 1,
      "connect": "EHZAPPV1.0.0.1",
      "describe": "",
      "qty": 13,
      "baseParam": [{
        "id": "url",
        "name": "服务地址",
        "type": "3",
        "value": "127.0.0.1:802/ehz/proxy"
      }]
    }],
    "total": 29
  },
  "result": null,
  "code": 0,
  "msg": null,
  "message": null
}
```

---

## 2. 根据标识符查询接口服务列表

**接口地址**: `POST /ESBREST/edge/app/getAppInterfaceList`
**作用**: API管理-根据标识符查询接口服务列表

### 请求参数

| 字段路径    | 类型      | 必填 | 说明                                 |
|-----------|---------|----|------------------------------------|
| appId    | integer | 否  | 所属应用 ID（UUID 格式），关联 getAppList 返回的 appId      |
| name      | string  | 否  | 查找关键字，用于模糊匹配应用名称进行搜索过滤         |
| page      | integer | 是  | 当前第几页，从 1 开始                    |
| size      | integer | 是  | 每页多少条数据                          |
**入参示例**:

```json
{
	"page": 1,
	"appId": "3710e1d4-7a76-40d0-84a5-81224d3fe892",
	"size": 10,
	"name": ""
}
```

### 返回字段

| 字段路径                              | 类型      | 必填 | 说明                                                                                      |
|-------------------------------------|---------|----|-----------------------------------------------------------------------------------------|
| errorCode                          | integer | 是  | 错误码，0=成功，非 0=失败                                                                         |
| errorMsg                           | string  | 是  | 错误信息，成功时为"执行成功！"                                                                        |
| return                             | Object  | 否  | 返回数据对象，失败时为 null                                                                        |
| return.list[]                      | array   | 是  | 接口服务记录列表                                                                                |
| return.list[].id                   | string  | 是  | 接口记录主键 UUID，唯一标识                                                                        |
| return.list[].appId               | string  | 是  | 所属应用 ID（UUID 格式），关联 getAppList 返回的 appId                                                |
| return.list[].name                 | string  | 是  | 接口名称，如"insertProductionPlan"展示用                                                         |
| return.list[].addr                 | string  | 是  | 接口地址/路由路径，与 name 通常相同，用于调用时指定                                                           |
| return.list[].state               | integer | 是  | 接口状态，1=启用，0=停用                                                                          |
| return.list[].describe            | string  | 是  | 接口描述说明                                                                                  |
| return.list[].method              | string  | 是  | HTTP 请求方法，枚举值：`POST`=POST；`GET`=GET；`PUT`=PUT                                           |
| return.list[].inParam[]           | array   | 是  | 入参定义列表，描述该接口接受的输入参数                                                                     |
| return.list[].inParam[].code      | string  | 是  | 参数标识/字段名，如"order_id"、"product_name"                                                     |
| return.list[].inParam[].name      | string  | 是  | 参数中文名称，如"订单编号"、"产品名称"                                                                   |
| return.list[].inParam[].type      | string  | 是  | 参数类型，枚举值：`integer`=整形；`number`=数值;  `datatime`=时间; `json`=json; `table`=表 `string`=字符串； |
| return.list[].inParam[].required  | integer | 是  | 是否必填，1=必填，0=非必填                                                                         |
| return.list[].inParam[].defaultVal | string | 是  | 参数默认值，未填写时使用此值                                                                          |
| return.list[].inParam[].describe  | string  | 是  | 参数描述说明                                                                                  |
| return.list[].outParam[]          | array   | 是  | 出参定义列表（当前通常为空数组）                                                                        |
| return.total                      | integer | 是  | 满足查询条件的接口服务记录总条数                                                                        |
| result                            | null    | 是  | 兼容字段，固定为 null                                                                           |
| code                              | integer | 是  | 兼容错误码，同 errorCode                                                                       |
| msg                               | null    | 是  | 兼容字段，固定为 null                                                                           |
| message                           | null    | 是  | 兼容字段，固定为 null                                                                           |

**返回示例**:

```json
{
  "errorCode": 0,
  "errorMsg": "执行成功！",
  "return": {
    "list": [{
      "id": "a80c558e-dff3-4976-aad4-37d0384abd11",
      "appId": "3710e1d4-7a76-40d0-84a5-81224d3fe892",
      "name": "insertProductionPlan",
      "addr": "insertProductionPlan",
      "state": 1,
      "describe": "",
      "method": "POST",
      "inParam": [{
        "code": "order_id",
        "name": "订单编号",
        "type": "string",
        "required": 1,
        "defaultVal": "",
        "describe": ""
      }, {
        "code": "product_name",
        "name": "产品名称",
        "type": "string",
        "required": 0,
        "defaultVal": "",
        "describe": ""
      }, {
        "code": "product_code",
        "name": "产品编码",
        "type": "string",
        "required": 0,
        "defaultVal": "",
        "describe": ""
      }],
      "outParam": []
    }],
    "total": 13
  },
  "result": null,
  "code": 0,
  "msg": null,
  "message": null
}
```

---

## 3. 获取单个接口文档

**接口地址**: `POST /ESBREST/faas/code/get_interface_doc`
**作用**: API管理-获取单个接口文档, 需要以md格式呈现

### 请求参数

| 字段路径  | 类型     | 必填 | 说明                                        |
|---------|--------|----|-------------------------------------------|
| addr    | string | 是  | 接口地址，精确匹配，填写接口服务列表中的 addr 字段，如"insertProductionPlan" |
| appName | string | 是  | 应用名称，精确匹配，填写接口所属应用的 name 字段，如"业务云函数管理"     |

**入参示例**:

```json
{
  "addr": "insertProductionPlan",
  "appName": "业务云函数管理"
}
```

### 返回字段

| 字段路径              | 类型     | 必填 | 说明                                       |
|---------------------|--------|----|------------------------------------------|
| errorCode           | integer | 是  | 错误码，0=成功，非 0=失败                          |
| errorMsg            | string  | 是  | 错误信息，成功时为"操作成功"                        |
| return              | Object  | 否  | 返回数据对象，失败时为 null                         |
| return.content      | string  | 是  | 接口文档内容（Markdown 格式），包含路径、描述、请求/响应参数说明 |
| return.appName      | string  | 是  | 应用名称，同请求参数 appName                       |
| return.addr         | string  | 是  | 接口地址，同请求参数 addr                          |
| result              | null    | 是  | 兼容字段，固定为 null                            |
| code                | integer | 是  | 兼容错误码，同 errorCode                         |
| msg                 | null    | 是  | 兼容字段，固定为 null                            |
| message             | null    | 是  | 兼容字段，固定为 null                            |

**返回示例**:

```json
{
  "errorCode": 0,
  "errorMsg": "操作成功",
  "return": {
    "content": "## insertProductionPlan\n\n### 接口路径\nPOST [http://gateway:80/ESBREST/edge/app/insertProductionPlan]\n\n### 接口描述\ninsertProductionPlan\n\n### 请求参数\n| 字段标识 | 字段名 | 类型 | 必填 | 事例 | 描述 |\n| --- | --- | --- | --- | --- | --- |\n| order_id | 订单编号 | 字符串 | 是 | \"\" | 订单编号 |\n\n### 响应参数\n无参数\n",
    "appName": "业务云函数管理",
    "addr": "insertProductionPlan"
  },
  "result": null,
  "code": 0,
  "msg": null,
  "message": null
}
```

---

## 4. 调用API管理接口服务

**接口地址**: `POST /ESBREST/edge/app/debugAppInterface`
**作用**: API管理-调用API管理接口服务，标准的数据流格式，用于平台标准功能配置
**备注**: 请求参数【inParam】来源于接口名【根据标识符查询接口服务列表】接口地址【/ESBREST/edge/app/getAppInterfaceList】下的返回值
         1.根据name 先判断state 如果是停用，则无法调用，则 找到 id 和appId 传递给请求接口，
         2.inParam下支持根据【name】找到【code】或者【code】传参； 【defaultVal】的值 需要根据【type】的类型进行验证，不符合提示类型错误；【required】必要参数验证

### 请求参数

| 字段路径              | 类型     | 必填 | 说明                                              | 
|---------------------|--------|----|-------------------------------------------------|
| appId               | string  | 是  | 应用 ID（UUID 格式），精确匹配，填写 getAppList 返回的 appId   | 
| id                  | string  | 是  | 接口记录 ID（UUID 格式），精确匹配，填写 getAppInterfaceList 返回的 id | 
| inParam[]           | array   | 是  | 入参列表，填写该接口实际调用时传递的参数                       | 
| inParam[].code      | string  | 是  | 参数标识，与 getAppInterfaceList 返回的 inParam[].code 对应  | 
| inParam[].type      | string  | 是  | 参数类型，枚举值：`string`=字符串；`integer`=整数；`number`=数值   | 
| inParam[].defaultVal | string | 是  | 参数默认值                                        | 
| callWay             | string  | 否  | 调用方式，枚举值：`debug`=调试模式；不传或其他值为正式调用        |  

**入参示例**:

```json
{
  "appId": "3710e1d4-7a76-40d0-84a5-81224d3fe892",
  "id": "a80c558e-dff3-4976-aad4-37d0384abd11",
  "inParam": [{
    "code": "order_id",
    "type": "string",
    "defaultVal": ""
  }],
  "callWay": "debug"
}
```

### 返回字段

| 字段路径         | 类型      | 必填 | 说明                         |
|----------------|---------|----|----------------------------|
| _ERR_CODE     | integer | 是  | 错误码，0=成功，非 0=失败          |
| _ERR_MSG      | string  | 是  | 错误信息，成功时为"操作成功！"          |
| return        | Object  | 否  | 返回数据对象，失败时结构依具体接口而定      |
| return.id     | string  | 是  | 调用标识/记录 ID                   |
| return.data   | Object  | 是  | 接口实际返回的业务数据对象，结构依具体接口而定 |

**返回示例**:

```json
{
  "_ERR_CODE": 0,
  "_ERR_MSG": "操作成功！",
  "return": {
    "id": "testfaas",
    "data": {}
  }
}
```

---

## 通用说明

### 错误码说明

| 错误码 | 说明       |
|-----|----------|
| 0   | 成功       |
| 400 | 请求参数错误   |
| 401 | 认证失败     |
| 404 | 设备不存在    |
| 408 | 请求超时     |
| 500 | 服务器内部错误  |
| 502 | 网关错误     |
| 503 | 服务不可用    |

### 错误响应格式

```json
{
  "errorCode": 400,
  "errorMsg": "参数错误",
  "return": null
}
```

---

## 完整请求示例

### cURL 示例

```bash
# 获取API管理应用接入列表
curl -X POST "https://api.jilian.com/ESBREST/edge/app/getAppList" \
  -H "Authorization: Bearer your-token" \
  -H "Sys-Apikey: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"page": 1, "size": 10}'

# 根据标识符查询接口服务列表
curl -X POST "https://api.jilian.com/ESBREST/edge/app/getAppInterfaceList" \
  -H "Authorization: Bearer your-token" \
  -H "Sys-Apikey: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"table_id": "faasbusi"}'

# 获取单个接口文档
curl -X POST "https://api.jilian.com/ESBREST/faas/code/get_interface_doc" \
  -H "Authorization: Bearer your-token" \
  -H "Sys-Apikey: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"addr": "insertProductionPlan", "appName": "业务云函数管理"}'

# 调用API管理接口服务
curl -X POST "https://api.jilian.com/ESBREST/edge/app/debugAppInterface" \
  -H "Authorization: Bearer your-token" \
  -H "Sys-Apikey: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"appId": "3710e1d4-7a76-40d0-84a5-81224d3fe892", "id": "a80c558e-dff3-4976-aad4-37d0384abd11", "inParam": [{"code": "order_id", "type": "string", "defaultVal": ""}], "callWay": "debug"}'
```

### Python 示例

```python
import requests

API_URL = "https://api.jilian.com"
TOKEN = "your-token"
API_KEY = "your-api-key"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Sys-Apikey": API_KEY,
    "Content-Type": "application/json"
}

# 获取API管理应用接入列表
payload = {"page": 1, "size": 10}
response = requests.post(f"{API_URL}/ESBREST/edge/app/getAppList", headers=headers, json=payload)
print(response.json())

# 根据标识符查询接口服务列表
payload = {"table_id": "faasbusi"}
response = requests.post(f"{API_URL}/ESBREST/edge/app/getAppInterfaceList", headers=headers, json=payload)
print(response.json())

# 获取单个接口文档
payload = {"addr": "insertProductionPlan", "appName": "业务云函数管理"}
response = requests.post(f"{API_URL}/ESBREST/faas/code/get_interface_doc", headers=headers, json=payload)
print(response.json())

# 调用API管理接口服务
payload = {
    "appId": "3710e1d4-7a76-40d0-84a5-81224d3fe892",
    "id": "a80c558e-dff3-4976-aad4-37d0384abd11",
    "inParam": [{"code": "order_id", "type": "string", "defaultVal": ""}],
    "callWay": "debug"
}
response = requests.post(f"{API_URL}/ESBREST/edge/app/debugAppInterface", headers=headers, json=payload)
print(response.json())
```
