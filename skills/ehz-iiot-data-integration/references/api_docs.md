# 极联设备管理 API 文档

## 接口配置

| 配置项     | 说明              | 环境变量      |
|---------|-----------------|-----------|
| API 地址  | 极联产品后端地址        | API_URL   |
| API Key | 认证密钥            | API_KEY   |
| Token   | Bearer 认证 Token | API_TOEKN |

## 通用请求头

```
Authorization: Bearer {token}
Sys-Apikey: {apikey}
Content-Type: application/json
```

## 接口清单

### 1. 数据存储管理-列表查询

**接口地址**: `GET /ESBREST/iiot/dataStorage/list`
**作用**: 数据存储管理-列表查询

**请求参数**:

| 参数       | 类型      | 必填 | 说明         | 默认值 |
|----------|---------|----|------------|-----|
| isPage   | integer | 否  | isPage     | 1   |
| keyword  | string  | 否  | 查找关键字,模糊搜索 |     |
| pageNo   | integer | 否  | 当前第几页      | 1   |
| pageSize | integer | 否  | 每页多少条数据    | 10  |
| tags     | string  | 否  | 标签标识       |     |

**入参示例**:

```string 带分页
tags=&pageNo=1&pageSize=10&keyword=
```

```string 不带分页
?isPage=0
```

**返回字段说明**:

| 字段名                                 | 类型        | 说明                             |
|-------------------------------------|-----------|--------------------------------|
| code                                | integer   | 返回代码                           |
| message                             | string    | 返回处理消息                         |
| requestId                           | string    | 请求Id                           |
| result                              | object    | 返回数据对象                         |
| result.records                      | Array     | 返回数据列表                         |
| result.records[].id                 | string    | 表名id                           |
| result.records[].tableId            | string    | 表标识符                           |
| result.records[].tableName          | string    | 表名中文                           |
| result.records[].entId              | string    | 企业号                            |
| result.records[].tableType          | string(1) | 表类型:1输入，2输出，0输入输出              |
| result.records[].type               | string    | 输出                             |
| result.records[].tags               | string    | 所属标签                           |
| result.records[].cfg                | string    | 输出配置                           |
| result.records[].referTable         | string    | 表绑定                            |
| result.records[].description        | string    | 表备注                            |
| result.records[].isSys              | boolean   | 是否系统表                          |
| result.records[].isPermanentStorage | boolean   | 数据保存时间(天) 0否，1是                |
| result.records[].dataSaveDays       | string    | 保存天数 只有 数据保存时间(天数) 是1(有期限)，才生效 |
| result.records[].cfgId              | string    | 连接配置id                         |
| result.records[].createBy           | string    | 创建人                            |
| result.records[].createTime         | string    | 创建时间                           |
| result.records[].updateBy           | string    | 修改人                            |
| result.records[].updateTime         | string    | 修改时间                           |
| result.total                        | integer   | 数据总条数                          |
| result.size                         | integer   | 每页多少条数据                        |
| result.current                      | integer   | 当前第几页                          |
| result.orders                       | integer   | 时间戳                            |
| result.optimizeCountSql             | boolean   | 成功标志                           |
| result.searchCount                  | integer   | 时间戳                            |
| result.countId                      | boolean   | 成功标志                           |
| result.maxLimit                     | integer   | 时间戳                            |
| result.pages                        | integer   | 一共几页                           |
| success                             | boolean   | 成功标志                           |
| timestamp                           | integer   | 时间戳                            |

**返回示例**:

```json
{
	"success": true,
	"message": "",
	"code": 200,
	"result": {
		"records": [{
			"id": "1643087355339046913",
			"createBy": "admin",
			"createTime": "2023-04-04 11:05:27",
			"updateBy": "admin",
			"updateTime": "2024-05-07 10:01:20",
			"entId": "hztest",
			"tableName": "工作流",
			"tableId": "_plan_t_flow_instance",
			"tableType": "0",
			"type": "mysql",
			"tags": "1",
			"cfg": "{\"host\": \"mysql\", \"port\": 3306, \"database\": \"ehzOS\", \"username\": \"root\", \"password\": \"vxWbUk5n3Sz7YFWgJRqTMA==\", \"type\": \"mysql\", \"charset\": \"utf8mb4\"}",
			"referTable": "_plan_t_flow_instance",
			"description": "工作流",
			"isSys": 0,
			"isPermanentStorage": null,
			"dataSaveDays": null,
			"cfgId": 1787663976914620400
		}],
		"total": 2,
		"size": 10,
		"current": 1,
		"orders": [],
		"optimizeCountSql": true,
		"searchCount": true,
		"countId": null,
		"maxLimit": null,
		"pages": 1
	},
	"timestamp": 1774935858801,
	"requestId": "8a4981749d408f08019d426bde711737"
}
```

---

### 2. 数据存储管理-获取表结构数据

**接口地址**: `GET /ESBREST/iiot/dataStorage/getTableStructure`
**作用**: 数据存储管理-获取表结构数据

**请求参数**:

| 参数       | 类型      | 必填 | 说明   | 默认值 |
|----------|---------|----|------|-----|
| isCopy   | integer | 否  | 是否复制 |     |
| table_id | string  | 是  | 表标识符 |     |

**入参示例**:

```string
table_id=HZ_TESTaa
```

**返回字段说明**:

| 字段名                                 | 类型        | 说明                                              |
|-------------------------------------|-----------|-------------------------------------------------|
| code                                | integer   | 返回代码                                            |
| message                             | string    | 返回处理消息                                          |
| requestId                           | string    | 请求Id                                            |
| result                              | object    | 返回数据对象                                          |
| result.id                           | string    | 表名id                                            |
| result.is_permanent_storage         | boolean   | 数据保存时间(天) 0否，1是                                 |
| result.cfg                          | string    | 输出配置                                            |
| result.data_save_days               | string    | 保存天数 只有 数据保存时间(天数) 是1(有期限)，才生效                  |
| result.description                  | string    | 表备注                                             |
| result.cfg_id                       | string    | 连接配置id                                          |_
| result.table_id                     | string    | 表标识符                                            |
| result.table_type                   | string(1) | 表类型:1输入，2输出，0输入输出                               |
| result.type                         | string    | 输出                                              |
| result.table_name                   | string    | 表名中文                                            |
| result.tags                         | string    | 所属标签                                            |
| result.refer_table                  | string    | 表绑定                                             |
| result.ent_id                       | string    | 企业号                                             |
| result.is_sys                       | boolean   | 是否系统表                                           |
| result.create_by                    | string    | 创建人                                             |
| result.create_time                  | string    | 创建时间                                            |
| result.updateBy                     | string    | 修改人                                             |
| result.update_time                  | string    | 创建时间                                            |
| result.tableFieldList               | Array     | 表字段列表                                           |
| result.tableFieldList[].id          | string    | 字段标识                                            |
| result.tableFieldList[].field       | string    | 字段识符                                            |
| result.tableFieldList[].name        | string    | 字段中文名                                           |
| result.tableFieldList[].type        | string    | 字段类型: integer:整型  number:数值 string:字符串  time:时间 |
| result.tableFieldList[].description | string    | 字段描述                                            |
| result.tableFieldList[].createBy    | string    | 创建人                                             |
| result.tableFieldList[].createTime  | string    | 创建时间                                            |
| result.tableFieldList[].updateBy    | string    | 修改人                                             |
| result.tableFieldList[].updateTime  | string    | 修改时间                                            |
| success                             | boolean   | 成功标志                                            |
| timestamp                           | integer   | 时间戳                                             |

**返回示例**:

```json
{
	"success": true,
	"message": "",
	"code": 200,
	"result": {
		"is_permanent_storage": null,
		"create_time": "2023-04-04 11:05:27",
		"cfg": "{\"host\": \"mysql\", \"port\": 3306, \"database\": \"ehzOS\", \"username\": \"root\", \"password\": \"vxWbUk5n3Sz7YFWgJRqTMA==\", \"type\": \"mysql\", \"charset\": \"utf8mb4\"}",
		"data_save_days": null,
		"description": "工作流",
		"cfg_id": 1787663976914620400,
		"table_id": "_plan_t_flow_instance",
		"type": "mysql",
		"table_name": "工作流",
		"tags": "1",
		"create_by": "admin",
		"refer_table": "_plan_t_flow_instance",
		"update_time": "2024-05-07 10:01:20",
		"ent_id": "hztest",
		"is_sys": 0,
		"tableFieldList": [{
			"id": null,
			"createBy": "admin",
			"createTime": "2023-04-04 11:06:38",
			"updateBy": null,
			"updateTime": null,
			"field": "status",
			"type": "string",
			"name": "流程实例当前状态",
			"description": ""
		}],
		"id": "1643087355339046913",
		"update_by": "admin",
		"table_type": "0"
	},
	"timestamp": 1774937726016,
	"requestId": "8a4981749d408f08019d42885c40195d"
}
```

---

### 3. 系统-标签表-获取标签树

**接口地址**: `GET /ESBREST/iiot/SystemTag/getTagsTree`
**作用**: 系统-标签表-获取数据存储类型的标签树

**请求参数**:

| 参数   | 类型     | 必填 | 说明   | 默认值     |
|------|--------|----|------|---------|
| type | string | 是  | 标签类型 | storage |


**入参示例**:

```string
type=storage
```

**返回字段说明**:

| 字段名                        | 类型      | 说明      |
|----------------------------|---------|---------|
| code                       | integer | 返回代码    |
| message                    | string  | 返回处理消息  |
| requestId                  | string  | 请求Id    |
| result                     | Array   | 返回数据列表  |
| result[].counts            | integer | 标签数量    |
| result[].childids          | string  | 子级标识符数组 |
| result[].id                | integer | 标签标识符   |
| result[].title             | string  | 标签名     |
| result[].type              | integer | 标签类型    |
| result[].key               | string  | 标签key   |
| result[].children          | Array   | 子级数据列表  |
| result[].children[].counts | integer | 标签数量    |
| result[].children[].id     | integer | 标签标识符   |
| result[].children[].title  | string  | 标签名     |
| result[].children[].type   | integer | 标签类型    |
| result[].children[].key    | string  | 标签key   |
| success                    | boolean | 成功标志    |
| timestamp                  | integer | 时间戳     |

**返回示例**:

```json
{
	"success": true,
	"message": "",
	"code": 200,
	"result": [{
		"children": [{
			"counts": 2,
			"id": "1",
			"title": "数据采集",
			"type": 1,
			"key": "8a4991099d42aced019d42d48c6c02f8"
		}],
		"counts": 6,
		"childids": "1,2,3,4",
		"id": "8a4991099d42aced019d42d48c6c02f9",
		"title": "基础平台",
		"type": 0,
		"key": "8a4991099d42aced019d42d48c6c02fa"
	}],
	"timestamp": 1774942719084,
	"requestId": "8a4991099d42aced019d42d48c6c0301"
}
```

---

### 4. 获取关联表数据

**接口地址**: `GET /ESBREST/iiot/dataStorage/getReferTableData`
**作用**: 数据存储管理-获取关联表数据，组合成表格数据格式,返回值 result.records 对象数据， key是标题，valude 是表格数据

**请求参数**:

| 参数        | 类型      | 必填 | 说明                                 | 默认值 |
|-----------|---------|----|------------------------------------|-----|
| condition | string  | 否  | 条件 无 等于 不等于 大于 大于等于 小于 小于等于 包含 不包含 |     |
| field     | string  | 否  | 表字段标识                              |     |
| pageNo    | integer | 否  | 当前第几页                              | 1   |
| pageSize  | integer | 否  | 每页多少条数据                            | 10  |
| table_id  | string  | 是  | 表标识符                               |     |
| value     | object  | 否  | value                              | 值   |

**入参示例**:

```string
pageNo=1&pageSize=10&table_id=m1120_device_status&field=&condition=&value=
```

**返回字段说明**:

| 字段名                       | 类型                        | 说明                          |
|---------------------------|---------------------------|-----------------------------|
| code                      | integer                   | 返回代码                        |
| message                   | string                    | 返回处理消息                      |
| requestId                 | string                    | 请求Id                        |
| result                    | object                    | 返回数据对象                      |
| success                   | boolean                   | 成功标志                        |
| timestamp                 | integer                   | 时间戳                         |
| result.total              | integer                   | 数据总条数                       |
| result.current            | integer                   | 当前第几页                       |
| result.pages              | integer                   | 一共几页                        |
| result.size               | integer                   | 每页多少条数据                     |
| result.records            | Array                     | 返回数据列表                      |
| result.records[].fileCode | string                    | 字段标识符 动态生成，根据查询表标识符,对应的中文名称 |
| result.records[].value    | string<动态生成，根据字段标识符对应的类型> | 字段值 动态生成，根据查询表标识符和字段标识符对应的值 |

**返回示例**:

```json
{
	"success": true,
	"message": "",
	"code": 200,
	"result": {
		"total": 8,
		"current": 1,
		"pages": 1,
		"size": 10,
		"records": [{
			"模型Id": "DEV001",
			"总开机率": null,
			"序号": 1,
			"开机时间": null,
			"预留字段1": null,
			"预留字段2": null,
			"总利用率": null,
			"更新时间": "2026-02-03 16:41:26",
			"自然时间": null,
			"运行效率": 100,
			"故障停机率": 50,
			"设备名称": "混料机",
			"预留字段3": null,
			"运行时间": "01:05:26",
			"创建时间": "2026-01-13 09:41:35",
			"空闲时间": null,
			"故障时间": "06:00:00"
		}]
	},
	"timestamp": 1775008181468,
	"requestId": "8a49804a9d454a98019d46bb6cdc09a3"
}
```
---

### 5. 数据存储管理-获取表字段信息

**接口地址**: `GET /ESBREST/iiot/dataStorage/tableFieldList`
**作用**: 数据存储管理-获取表字段信息

**请求参数**:

| 参数       | 类型      | 必填 | 说明         | 默认值 |
|----------|---------|----|------------|-----|
| isPage   | integer | 否  | isPage     | 1   |
| keyword  | string  | 否  | 查找关键字,模糊搜索 |     |
| pageNo   | integer | 否  | 当前第几页      | 1   |
| pageSize | integer | 否  | 每页多少条数据    | 10  |
| tags     | string  | 否  | 标签标识       |     |
| table_id | string  | 是  | 表标识符       |     |


**入参示例**:

**分页查询**

```string  
pageNo=1&pageSize=10&table_id=HZ_TESTaa&keyword=
```

**无分页查询**
```string 
isPage=0&table_id=HZ_TESTaa&keyword=
```

**返回字段说明**:

| 字段名                          | 类型      | 说明      |
|------------------------------|---------|---------|
| code                         | integer | 返回代码    |
| message                      | string  | 返回处理消息  |
| requestId                    | string  | 请求Id    |
| result                       | object  | 返回数据对象  |
| result.records               | Array   | 返回数据列表  |
| result.records[].id          | string  | 表字段id   |
| result.records[].field       | string  | 表字段标识符  |
| result.records[].type        | string  | 表字段类型   |
| result.records[].name        | string  | 表字段中文名称 |
| result.records[].description | string  | 表备注     |
| result.records[].createBy    | string  | 创建人     |
| result.records[].createTime  | string  | 创建时间    |
| result.records[].updateBy    | string  | 修改人     |
| result.records[].updateTime  | string  | 修改时间    |
| success                      | boolean | 成功标志    |
| timestamp                    | integer | 时间戳     |

**返回示例**:

```json
{
	"success": true,
	"message": "",
	"code": 200,
	"result": {
		"records": [{
			"id": "2029850122790449153",
			"createBy": "admin",
			"createTime": "2026-03-06 17:22:37",
			"updateBy": null,
			"updateTime": null,
			"field": "cca",
			"type": "string",
			"name": "cca",
			"description": "cca"
		}]
	},
	"timestamp": 1775009169295,
	"requestId": "8a49804a9d454a98019d46ca7f8f0a69"
}
```

---

## 6. 数据存储管理-查询所有表关系列表

**接口地址**: `post /ESBREST/faas/code/getTableRelationshipList`
**作用**: 数据存储管理-查询所有表列表

**请求参数**:

| 参数           | 类型      | 必填 | 说明      | 默认值 |
|--------------|---------|----|---------|-----|
| mainTable    | string  | 否  | 主表名     |     |
| foreignTable | string  | 否  | 从表名     |     |
| page         | integer | 否  | 当前第几页   | 1   |
| pageSize     | integer | 否  | 每页多少条数据 | 10  |

**入参示例**:

```json
{"page": 1, "pageSize": 10, "mainTable": "", "foreignTable": ""}
```

**返回字段说明**:

| 字段名                   | 类型     | 说明        |
|-----------------------|--------|-----------|
| errorCode             | Number | 错误码，0表示成功 |
| errorMsg              | String | 错误消息      |
| return                | Array  | 表列表       |
| return[].tableName    | String | 表名        |
| return[].tableComment | String | 表注释       |

**返回示例**:

```json
{
  "errorCode": 0,
  "errorMsg": "success",
  "return": [
    {
      "tableName": "sales_order",
      "tableComment": "销售订单表"
    },
    {
      "tableName": "order_detail",
      "tableComment": "订单明细表"
    }
  ]
}
```

---

## 7. 获取关系详情接口

**接口地址**: `post /ESBREST/faas/code/getTableRelationshipDetail`
**作用**: 数据存储管理-获取关系详情接口

**请求参数**:

| 参数名 | 类型  | 必填 | 说明   | 默认值 |
|-----|-----|----|------|-----|
| id  | int | 是  | 关系ID |     |

**入参示例**:

```json  
{"id":19}
```

**返回字段说明**:

| 字段名                                  | 类型     | 说明                                            |
|--------------------------------------|--------|-----------------------------------------------|
| errorCode                            | Number | 错误码，0表示成功                                     |
| errorMsg                             | String | 错误消息                                          |
| return                               | 对象     | 表对象                                           |
| return.id                            | String | 关系ID                                          |
| return.mainTable                     | String | 主表名                                           |
| return.foreignTable                  | String | 从表名                                           |
| return.relationshipType              | String | 关系类型：关系类型：one-to-one/one-to-many/many-to-many |
| return.relationshipDescription       | String | 否:关系描述                                        |
| return.relationshipDescription       | String | 关系描述                                          |
| return.fieldMappings                 | Array  | 字段映射数组                                        |
| return.fieldMappings[].id            | String | 字段映射ID                                        |
| return.fieldMappings[].main_field    | String | 主表字段                                          |
| return.fieldMappings[].foreign_field | String | 从表字段                                          |
| return.fieldMappings[].mapping_order | Number | 映射顺序                                          |
| result.createBy                      | string | 创建人                                           |
| result.createTime                    | string | 创建时间                                          |
| result.updateBy                      | string | 修改人                                           |
| result.updateTime                    | string | 修改时间                                          |


**返回示例**:

```json
{
  "errorCode": 0,
  "errorMsg": "success",
  "return": [
    {
      "id": 11,
      "mainTable": "TEST__sys_t_role_data",
      "foreignTable": "TEST_sys_role_permission",
      "relationshipType": "one-to-many",
      "relationshipDescription": "",
      "fieldMappings": [
        {
          "id": 15,
          "main_field": "roleid",
          "foreign_field": "role_id",
          "mapping_order": 1
        }
      ],
      "createdBy": "admin",
      "createdTime": "2026-03-10 10:04:43",
      "updatedBy": "admin",
      "updatedTime": "2026-03-10 10:04:43"
    }
  ]
}
```

## 通用说明

### 错误码说明

| 错误码 | 说明      |
|-----|---------|
| 0   | 成功      |
| 400 | 请求参数错误  |
| 401 | 认证失败    |
| 404 | 设备不存在   |
| 408 | 请求超时    |
| 500 | 服务器内部错误 |
| 502 | 网关错误    |
| 503 | 服务不可用   |

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
# 获取设备列表
curl -X POST "https://api.jilian.com/ESBREST/faas/code/getEqpList" \
  -H "Authorization: Bearer your-token" \
  -H "Sys-Apikey: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"pageIndex": 1, "page": 20}'

# 设备反控（写入数据）
curl -X POST "https://api.jilian.com/ESBREST/faas/code/setData" \
  -H "Authorization: Bearer your-token" \
  -H "Sys-Apikey: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"attr": "MOMTest.temperature", "value": 30}'

# 获取设备实时数据
curl -X POST "https://api.jilian.com/ESBREST/faas/code/getRealTimeDatas" \
  -H "Authorization: Bearer your-token" \
  -H "Sys-Apikey: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{"attrs": ["MOMTest.temperature", "MOMTest.pressure"]}'
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

# 获取设备列表
payload = {"pageIndex": 1, "page": 20}
response = requests.post(f"{API_URL}/ESBREST/faas/code/getEqpList", headers=headers, json=payload)
print(response.json())

# 设备反控（写入数据）
payload = {"attr": "MOMTest.temperature", "value": 30}
response = requests.post(f"{API_URL}/ESBREST/faas/code/setData", headers=headers, json=payload)
print(response.json())

# 获取设备实时数据
payload = {"attrs": ["MOMTest.temperature", "MOMTest.pressure"]}
response = requests.post(f"{API_URL}/ESBREST/faas/code/getRealTimeDatas", headers=headers, json=payload)
print(response.json())
```