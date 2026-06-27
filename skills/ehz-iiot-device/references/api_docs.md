# 极联设备管理 API 文档

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

## 接口清单

### 1. 获取设备列表

**接口地址**: `POST /ESBREST/faas/code/getEqpList`
**作用**: 获取平台中所有设备的基础信息列表，支持分区、在线状态、告警状态、关键字等条件筛选

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| areaId | String | 否 | 分区标识，为空时默认使用系统根分区 | 空 |
| pageIndex | Integer | 是 | 当前页数 | 1 |
| page | Integer | 是 | 每页条数 | 20 |
| keyword | String | 否 | 关键字，支持设备名称、sn、eid、设备编号模糊匹配 | 空 |
| online | Integer | 否 | 在线状态：1=在线；0=离线；-1=未接入；空=全部 | 空 |
| alarm | Integer | 否 | 告警状态：1=有告警 | 空 |
| emodelid | String | 否 | 设备型号标识 | 空 |

**入参示例**:

```json
{
    "areaId": "",
    "pageIndex": 1,
    "page": 20,
    "keyword": "",
    "online": "",
    "alarm": "",
    "emodelid": ""
}
```

**返回示例**:

```json
{
    "errorCode": 0,
    "errorMsg": "操作成功",
    "times": "mySql总耗时 -> 0.123 秒。Redis总耗时 -> 0.005 秒。",
    "return": {
        "datas": [
            {
                "sn": "edgebox1022.test01",
                "code": "MOMTest",
                "emodelid": "ZDT3CBQWS7",
                "eid": "IJJ2Q7IRQ8",
                "name": "MOM测试设备",
                "emodelName": "test01",
                "isFollow": 0,
                "location": "{}",
                "cards": "[\"defaultCard\"]",
                "ico": "img/emodel_default.png",
                "areaId": "93",
                "explain": "",
                "updateDt": "2026-03-16 10:17:58",
                "areaName": "设备分区",
                "areaPath": "设备分区",
                "entId": "hztest",
                "online": 1,
                "totalAlarm": 0,
                "lastRefreshTime": "2026-03-16 16:52:16",
                "refreshTime": "2026-03-16 16:52:16"
            }
        ],
        "pageIndex": 1,
        "pageTotal": 7,
        "datasTotal": 137,
        "onlineTotal": 6
    }
}
```

**返回字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| errorCode | Integer | 错误码，0=成功，-1000=系统异常 |
| errorMsg | String | 错误消息 |
| times | String | 性能耗时信息（MySQL + Redis） |
| return.datas | Array | 设备数据列表 |
| return.datas[].sn | String | sn接入号 |
| return.datas[].code | String | 设备编号 |
| return.datas[].emodelid | String | 设备型号ID |
| return.datas[].eid | String | 设备唯一标识 |
| return.datas[].name | String | 设备名称 |
| return.datas[].emodelName | String | 设备型号名称 |
| return.datas[].isFollow | Integer | 是否关注：1=关注，0=未关注 |
| return.datas[].location | String | 设备位置（JSON格式） |
| return.datas[].cards | String | 卡片配置（JSON格式数组） |
| return.datas[].ico | String | 设备图标路径 |
| return.datas[].areaId | String | 分区ID |
| return.datas[].explain | String | 设备说明 |
| return.datas[].updateDt | String | 数据更新时间 |
| return.datas[].areaName | String | 分区名称 |
| return.datas[].areaPath | String | 分区路径 |
| return.datas[].entId | String | 企业ID |
| return.datas[].online | Integer | 在线状态：1=在线，0=离线，-1=未接入 |
| return.datas[].totalAlarm | Integer | 告警总数 |
| return.datas[].lastRefreshTime | String | 最后刷新时间 |
| return.datas[].refreshTime | String | 刷新时间 |
| return.pageIndex | Integer | 当前页数 |
| return.pageTotal | Integer | 总页数 |
| return.datasTotal | Integer | 总记录数 |
| return.onlineTotal | Integer | 在线设备数 |


### 2. 设备反控（写入数据）

**接口地址**: `POST /ESBREST/faas/code/setData`
**作用**: 向指定设备属性下发控制指令，实现设备反控

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| attr | String | 是 | 属性标识，格式：{设备编号}.{属性ID} | 无 |
| value | String/Number | 是 | 写入的值 | 无 |

**入参示例**:

```json
{
    "attr": "MOMTest.temperature",
    "value": 30
}
```

**返回示例**:

```json
{
    "errorCode": 0,
    "errorMsg": "操作成功"
}
```

**返回字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| errorCode | Integer | 错误码，0=成功，-1=设备不存在，-1002=反控失败 |
| errorMsg | String | 错误消息 |

**注意事项**:
- attr 格式为 `{code}.{attrId}`，其中 code 为设备编号，attrId 为属性标识
- 反控操作会通过 ESB 调用 ppu_gateway 进行下发
- 操作记录会自动写入 `recordInverse` 函数进行审计

---

### 3. 获取设备实时数据

**接口地址**: `POST /ESBREST/faas/code/getRealTimeDatas`
**作用**: 批量获取设备属性的实时数据（最新值和刷新时间）

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| attrs | Array\<String\> | 是 | 属性标识数组，格式：{设备编号}.{属性ID} | 无 |

**入参示例**:

```json
{
    "attrs": ["MOMTest.temperature", "MOMTest.pressure"]
}
```

**返回示例**:

```json
{
    "errorCode": 0,
    "errorMsg": "操作成功!",
    "return": [
        {
            "attr": "MOMTest.temperature",
            "value": "25.6",
            "refreshTime": "2023-12-17 10:56:07"
        },
        {
            "attr": "MOMTest.pressure",
            "value": "101.325",
            "refreshTime": "2023-12-17 10:56:07"
        }
    ]
}
```

**返回字段说明**:

| 字段 | 类型 | 说明 |
|------|------|------|
| errorCode | Integer | 错误码，0=成功，-1=属性参数为空，-2=格式错误/设备不存在，-1000=系统异常 |
| errorMsg | String | 错误消息 |
| return | Array | 实时数据数组 |
| return[].attr | String | 属性标识 |
| return[].value | String | 属性当前值，为空表示无数据 |
| return[].refreshTime | String | 刷新时间（格式：yyyy-MM-dd HH:mm:ss，无数据时为 1970-01-01 08:00:00） |

**注意事项**:
- attrs 数组中每个元素格式必须为 `{code}.{attrId}`
- 设备编号和属性ID之间用 `.` 分隔
- 数据来源为 Redis 缓存，缓存中无数据时 value 返回空字符串

---

### 4. getEquipmentRtStatus - 获取设备实时状态

**接口地址**: `POST /ESBREST/faas/code/getEquipmentRtStatus`
**作用**: 批量获取设备的实时状态信息，包括在线状态、位置、告警数量等。

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| eids | Array | 是 | 设备EID数组 | |

**入参示例**:

```json
{
  "eids": ["eid_001", "eid_002", "eid_003"]
}
```

**返回参数**:

| 字段名            | 类型 | 说明 |
|----------------|------|------|
| errorCode      | Number | 错误码，0表示成功 |
| errorMsg       | String | 错误消息 |
| return         | Array | 设备状态列表 |
| return[].eid   | String | 设备EID |
| return[].iccid          | String | SIM卡ICCID |
| return[].isFollow       | String | 是否关注 |
| return[].lastRefreshTime | String | 最后刷新时间（UTC格式） |
| return[].location       | Object/String | 设备位置 |
| return[].online         | Number | 在线状态：1-在线，0-离线 |
| return[].totalAlarm     | Number | 告警数量 |

**返回字段 Array 项说明**:

| 字段名 | 类型 | 说明 |
|-------|------|------|


**返回示例**:

```json
{
  "errorCode": 0,
  "errorMsg": "操作成功",
  "return": [
    {
      "eid": "eid_001",
      "iccid": "89860000000000000000",
      "isFollow": "1",
      "lastRefreshTime": "2024-01-15T08:30:00.000Z",
      "online": 1,
      "totalAlarm": 0
    }
  ]
}
```
---

### 5. getEqpListNewTag - 根据标签获取设备列表

**接口地址**: `POST /ESBREST/faas/code/getEqpListNewTag`
**作用**: 根据设备标签分组ID或标签ID获取设备列表，支持与getEqpList相同的筛选、分页功能。

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| tagId | String | 是 | 标签ID（与groupId二选一） | |
| groupId | String | 是 | 标签分组ID（与tagId二选一） | |
| pageIndex | Number | 是 | 当前页码 | |
| page | Number | 是 | 每页条数 | |
| keyword | String | 是 | 关键词（设备名称/编号/SN/EID） | |
| online | Number | 否 | 在线状态筛选：1-在线，0-离线 | - |
| alarm | Number | 否 | 告警筛选：1-仅显示有告警设备 | - |
| emodelid | String | 否 | 设备模型ID | - |

**入参示例**:

```json
{
  "tagId": "tag_001",
  "groupId": "",
  "pageIndex": 1,
  "page": 20,
  "keyword": "",
  "alarm": 1
}
```

**返回参数**:

| 字段名 | 类型 | 说明                |
|-------|------|-------------------|
| errorCode | Number | 错误码，0表示成功         |
| errorMsg | String | 错误消息              |
| times | String | 耗时统计（MySQL/Redis） |
| return | Object | 返回数据              |
| return.datas | Array | 设备列表              |
| return.datas[].sn | String | 设备接入号             |
| return.datas[].code                   | String | 设备编号              |
| return.datas[].eid                    | String | 设备EID             |
| return.datas[].name                  | String | 设备名称              |
| return.datas[].emodelName             | String | 设备模型名称            |
| return.datas[].online                 | String | 设备在线状态            |
| return.datas[].totalAlarm          | Number | 设备告警状态            |
| return.pageIndex | Number | 当前页码              |
| return.pageTotal | Number | 总页数               |
| return.datasTotal | Number | 总记录数              |
| return.onlineTotal | Number | 在线设备数             |

**返回示例**:

```json
{
  "errorCode": 0,
  "errorMsg": "操作成功",
  "times": "mySql总耗时 -> 0.150 秒。Redis总耗时 -> 0.010 秒。",
  "return": {
    "datas": [
      {
        "sn": "SN001",
        "code": "CNC001",
        "eid": "eid_12345",
        "name": "1号加工中心",
        "emodelName": "CNC加工中心",
        "online": 1,
        "totalAlarm": 2
      }
    ],
    "pageIndex": 1,
    "pageTotal": 3,
    "datasTotal": 50,
    "onlineTotal": 40
  }
}
```

---

### 6. getAlarmHistoryData - 获取告警历史数据

**接口地址**: `POST /ESBREST/faas/code/getAlarmHistoryData`
**作用**: 查询设备的告警历史记录，支持多条件筛选、分页、排序。

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| areaId | String | 是 | 分区ID | |
| pageIndex | Number | 是 | 当前页码 | |
| pageSize | Number | 是 | 每页条数 | |
| topic | String | 否 | 告警名称（模糊匹配） | - |
| level | Number | 否 | 告警级别 | - |
| status | Number | 否 | 告警状态：1-未清除，0-已清除 | - |
| eid | String | 否 | 设备EID | - |
| code | String | 否 | 设备编号（模糊匹配） | - |
| emodelid | String | 否 | 设备模型ID | - |
| startTime | String | 否 | 开始时间（UTC格式） | - |
| endTime | String | 否 | 结束时间（UTC格式） | - |
| isConfirmed | Number | 否 | 确认状态 | - |
| dataSrc | String | 否 | 数据来源 | - |
| label | String | 否 | 标签 | - |
| modelCode | String | 否 | 模型编号 | - |
| name | String | 否 | 设备名称（模糊匹配） | - |
| modelName | String | 否 | 模型名称（模糊匹配） | - |

**入参示例**:

```json
{
  "areaId": "area_001",
  "pageIndex": 1,
  "pageSize": 20,
  "status": 1,
  "level": 2,
  "startTime": "2024-01-01T00:00:00.000Z",
  "endTime": "2024-01-31T23:59:59.000Z"
}
```

**返回参数**:

| 字段名                    | 类型 | 说明 |
|------------------------|------|------|
| errorCode              | Number | 错误码，0表示成功 |
| errorMsg               | String | 错误消息 |
| return                 | Object | 返回数据 |
| return.datas           | Array | 告警列表 |
| return.datas[].alarmId | String | 告警ID（ASN） |
| return.datas[].topic                  | String | 告警名称 |
| return.datas[].level                  | String | 告警级别 |
| return.datas[].status                 | String | 告警状态（value值） |
| return.datas[].makeTimestamp          | Number | 告警产生时间戳 |
| return.datas[].clearTimestamp         | Number | 告警清除时间戳 |
| return.datas[].isConfirmed            | Number | 确认状态 |
| return.datas[].relationDatas          | Array | 关联数据 |
| return.datas[].clearRelationDatas     | Array | 清除关联数据 |
| return.datas[].field1~field10         | String | 自定义扩展字段 |
| return.datas[].dataSrc                | String | 数据来源 |
| return.datas[].eventId                | String | 事件ID |
| return.datas[].eqptName               | String | 设备名称 |
| return.datas[].eid                    | String | 设备EID |
| return.datas[].emodelid               | String | 设备模型ID |
| return.datas[].emodelName             | String | 设备模型名称 |
| return.datas[].areaId                 | String | 分区ID |
| return.datas[].areaPath               | String | 分区路径 |
| return.datas[].code                   | String | 设备编号 |
| return.datasTotal      | Number | 总记录数 |
| return.pageTotal       | Number | 总页数 |
| return.pageIndex       | Number | 当前页码 |



**返回示例**:

```json
{
  "errorCode": 0,
  "errorMsg": "",
  "return": {
    "datas": [
      {
        "alarmId": "ASN_001",
        "topic": "温度过高告警",
        "level": "2",
        "status": "1",
        "makeTimestamp": 1672531200000,
        "eid": "eid_001",
        "eqptName": "1号加工中心",
        "relationDatas": [],
        "clearRelationDatas": []
      }
    ],
    "datasTotal": 100,
    "pageTotal": 5,
    "pageIndex": 1
  }
}
```

---

### 7. getHistoryDataByOrder - 获取设备历史数据

**接口地址**: `POST /ESBREST/faas/code/getHistoryDataByOrder`
**作用**: 获取指定设备的历史数据（分页），支持InfluxDB/Magus等时序数据库，支持最多8个属性同时查询。

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| eid | String | 是 | 设备EID（与code二选一） | |
| code | String | 否 | 设备编号（与eid二选一） | - |
| oids | Array | 是 | 属性OID数组，格式：`属性ID` 或 `设备EID.属性ID` | |
| startTime | String | 是 | 开始时间（UTC格式：YYYY-MM-DDTHH:MM:SS.000Z） | |
| endTime | String | 是 | 结束时间（UTC格式：YYYY-MM-DDTHH:MM:SS.000Z） | |
| interval | Number | 是 | 降采样时间间隔（毫秒） | |
| pageIndex | Number | 是 | 当前页码 | |
| pageSize | Number | 是 | 每页条数 | |
| btCall | String | 否 | 奔腾调用标识（扩展时间范围至15天） | - |

**入参示例**:

```json
{
  "eid": "eid_12345",
  "oids": ["temperature", "pressure"],
  "startTime": "2024-01-01T00:00:00.000Z",
  "endTime": "2024-01-07T00:00:00.000Z",
  "interval": 3600000,
  "pageIndex": 1,
  "pageSize": 100
}
```

**返回参数**:

| 字段名 | 类型 | 说明 |
|-------|------|------|
| errorCode | Number | 错误码，0表示成功 |
| errorMsg | String | 错误消息 |
| return | Object | 返回数据 |
| return.datas | Array | 历史数据列表 |
| return.datas[].timestamp | Number | 毫秒时间戳 |
| return.datas[].time | String | 时间字符串 |
| return.datas[].name | String | 属性名称 |
| return.datas[].value | String/Number | 属性值 |
| return.pageIndex | Number | 当前页码 |
| return.pageTotal | Number | 总页数 |
| return.datasTotal | Number | 总记录数 |
| return.name | Array | 属性名称列表 |


**返回示例**:

```json
{
  "errorCode": 0,
  "errorMsg": "操作成功!",
  "return": {
    "datas": [
      {"timestamp": 1672531200000, "time": "2024-01-01T00:00:00.000Z", "name": "温度(℃)", "value": 25.5},
      {"timestamp": 1672534800000, "time": "2024-01-01T01:00:00.000Z", "name": "温度(℃)", "value": 26.0}
    ],
    "pageIndex": 1,
    "pageTotal": 1,
    "datasTotal": 168,
    "name": ["温度(℃)", "压力(MPa)"]
  }
}
```


## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 400 | 请求参数错误 |
| 401 | 认证失败 |
| 404 | 设备不存在 |
| 408 | 请求超时 |
| 500 | 服务器内部错误 |
| 502 | 网关错误 |
| 503 | 服务不可用 |

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