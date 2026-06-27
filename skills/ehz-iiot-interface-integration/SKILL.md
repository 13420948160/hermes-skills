---
name: ehz-iiot-interface-integration
description: 极联平台接口管理集成 API 技能，支持应用接入列表、接口服务列表查询、接口文档获取和接口调试调用。
license: MIT
metadata:
  author: "ehz"
  version: "1.0.0"
---

# ehz-iiot-interface-integration 技能使用说明

封装极联平台接口管理集成 API，支持 API 管理应用接入列表、接口服务列表查询、接口文档获取和接口调试调用。

## 一、环境配置

### 1.1 复制环境变量模板

```bash
cd skills/ehz-iiot-interface-integration
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

本技能接口根据路径前缀分为两类，请求参数和返回值格式不同：

### 类型一：/ESBREST/edge/ 或 /ESBREST/faas/ 前缀接口（edge/faas 类型）

请求方式：POST
请求参数：必须包装在 `{ apikey: "", request: { ... } }` 结构中
返回值格式：
```json
{
  "errorCode": 0,
  "errorMsg": "操作成功",
  "return": { ... }
}
```

### 类型二：/ESBREST/iiot/ 前缀接口（iiot 类型）

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

---

## 三、接口清单

| # | 接口类型 | 方法 | 接口地址 | 说明 |
|---|---------|------|---------|------|
| 1 | edge | POST | `/ESBREST/edge/app/getAppList` | 获取API管理应用接入列表 |
| 2 | edge | POST | `/ESBREST/edge/app/getAppInterfaceList` | 根据标识符查询接口服务列表 |
| 3 | faas | POST | `/ESBREST/faas/code/get_interface_doc` | 获取单个接口文档 |
| 4 | edge | POST | `/ESBREST/edge/app/debugAppInterface` | 调用API管理接口服务 |

---

## 四、查询命令

### 4.1 查看所有可用命令

```bash
cd skills/ehz-iiot-interface-integration
python scripts/client.py --help
```

### 4.2 获取API管理应用接入列表（edge 类型）

```bash
# 默认分页（第一页，每页10条）
python scripts/client.py app-list

# 关键字搜索
python scripts/client.py app-list --name 业务云函数

# 自定义分页
python scripts/client.py app-list --page 1 --size 20
```

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| name  | string  | 否 | 查找关键字，模糊匹配应用名称进行搜索过滤 | |
| page  | integer | 是 | 当前第几页，从 1 开始 | 1 |
| size  | integer | 是 | 每页多少条数据 | 10 |

**返回字段**: `errorCode`, `errorMsg`, `return.list[]`, `return.total`

---

### 4.3 根据标识符查询接口服务列表（edge 类型）

```bash
# 按应用ID查询
python scripts/client.py app-interface-list \
  --app-id 3710e1d4-7a76-40d0-84a5-81224d3fe892 \
  --page 1 --size 10

# 关键字搜索
python scripts/client.py app-interface-list --name insertProductionPlan
```

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| appId | string | 否 | 所属应用 ID（UUID 格式），关联 getAppList 返回的 appId | |
| name  | string | 否 | 查找关键字，模糊匹配接口名称进行搜索过滤 | |
| page  | integer | 是 | 当前第几页，从 1 开始 | 1 |
| size  | integer | 是 | 每页多少条数据 | 10 |

**返回字段**: `errorCode`, `errorMsg`, `return.list[].inParam[]`, `return.total`

---

### 4.4 获取单个接口文档（faas 类型）

```bash
python scripts/client.py get-interface-doc \
  --addr insertProductionPlan \
  --app-name 业务云函数管理
```

**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| addr    | string | 是 | 接口地址，精确匹配，填写接口服务列表中的 addr 字段 | |
| appName | string | 是 | 应用名称，精确匹配，填写接口所属应用的 name 字段 | |

**返回字段**: `errorCode`, `errorMsg`, `return.content`, `return.appName`, `return.addr`

---

### 4.5 调用API管理接口服务（edge 类型）

```bash
python scripts/client.py debug-app-interface \
  --app-id 3710e1d4-7a76-40d0-84a5-81224d3fe892 \
  --id a80c558e-dff3-4976-aad4-37d0384abd11 \
  --in-param '[{"code": "order_id", "type": "string", "defaultVal": ""}]' \
  --call-way debug
```

```bash
python scripts/client.py debug-app-interface \
  --app-id ccc68ae2-e412-4fd2-a94a-c33f40779a49 \
  --id 789f8adf-2a3e-459d-a010-8d1406a751f4 \
  --in-param '[{"code":"pageNo","type":"integer","defaultVal":"1"},{"code":"pageSize","type":"integer","defaultVal":"10"}]' \
  --call-way debug
```


**请求参数**:

| 参数 | 类型 | 必填 | 说明 | 默认值 |
|------|------|------|------|--------|
| appId    | string | 是 | 应用 ID（UUID 格式），精确匹配，填写 getAppList 返回的 appId | |
| id       | string | 是 | 接口记录 ID（UUID 格式），精确匹配，填写 getAppInterfaceList 返回的 id | |
| inParam  | array  | 是 | 入参列表，JSON 数组格式 | |
| callWay  | string | 否 | 调用方式，`debug`=调试模式，不传或其他值为正式调用 | |

**返回字段**: `_ERR_CODE`, `_ERR_MSG`, `return.id`, `return.data`

---

## 五、返回格式

### edge/faas 类型成功

```json
{
  "errorCode": 0,
  "errorMsg": "执行成功！",
  "return": { ... }
}
```

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

### 错误格式

```json
{
  "errorCode": 400,
  "errorMsg": "参数错误",
  "return": null
}
```

或

```json
{
  "success": false,
  "message": "错误描述",
  "code": 500
}
```

---

## 六、常见错误码排查

| 错误码 | 说明 | 排查方法 |
|--------|------|---------|
| 401 | 认证失败 | 检查 SECRET_ID / SECRET_KEY 是否正确 |
| 408 | 请求超时 | 检查网络连通性或 API_URL 是否正确 |
| 502 | 响应非 JSON | 服务器异常，检查 API 服务状态 |
| 503 | 无法连接服务器 | 检查 API_URL 是否可达 |
| 404 | 命令未找到 | 检查命令拼写，可使用 `--help` 查看可用命令 |
| 500 | 未知错误 | 查看 errorMsg 详情，必要时开启 DEBUG 日志 |

---

## 七、测试

```bash
cd skills/ehz-iiot-interface-integration
# 运行所有测试
python scripts/test_client.py

# 输出报告到文件（文本 + JSON）
python scripts/test_client.py -o test_report.txt 2>&1

# 运行指定测试（支持模糊匹配）
python scripts/test_client.py app-list

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
| 应用接入列表 | `python scripts/client.py app-list` |
| 接口服务列表 | `python scripts/client.py app-interface-list --app-id <UUID>` |
| 接口文档 | `python scripts/client.py get-interface-doc --addr <接口地址> --app-name <应用名>` |
| 调试接口服务 | `python scripts/client.py debug-app-interface --app-id <UUID> --id <接口ID> --in-param '<JSON>'` |
| 运行测试 | `python scripts/test_client.py` |
