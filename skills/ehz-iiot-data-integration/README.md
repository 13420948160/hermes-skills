# ehz-iiot-data-integration 技能使用说明

封装极联平台数据集成 API，支持数据存储列表查询、表结构获取、标签树获取、关联表数据查询及表关系管理。

## 一、环境配置

### 1.1 复制环境变量模板

```bash
cd skills/ehz-iiot-data-integration
cp .env.example .env
```

### 1.2 编辑 `.env` 文件，填入实际值

| 变量名                 | 说明           | 示例                              |
|---------------------|--------------|---------------------------------|
| API_URL             | API 服务器地址    | https://jilian-sit.ehzcloud.com |
| ACCOUNT_ID          | 极联平台账号       | admin                           |
| SECRET_ID           | 密钥ID         | hziot                           |
| SECRET_KEY          | 密钥KEY        | your_secret_key_here            |
| TOKEN_VALID_SECONDS | Token 有效期（秒） | 900                             |

> **提示**：如不创建 `.env` 文件，程序会自动读取系统环境变量，等效于已 export 所有变量。

**认证说明**：`TOKEN` 无需手动配置，客户端启动时会自动调用 `/ESBREST/faas/code/getAccessToken` 接口换取，token 有效期 15 分钟，客户端会自动刷新。

---

## 二、API 类型说明

本技能包含两类接口，请求参数和返回值格式不同：

### 类型一：/ESBREST/iiot/ 前缀接口

请求方式：GET（参数放 URL query string）或 POST（参数放 JSON body）
请求参数：直接 JSON 对象
返回值格式：`{success, message, code, result}`

### 类型二：/ESBREST/faas/ 前缀接口

请求方式：POST
请求参数：必须包装在 `{apikey: "", request: {...}}` 结构中
返回值格式：`{errorCode, errorMsg, return}`

---

## 三、查询命令

### 3.1 查看所有可用命令

```bash
cd skills/ehz-iiot-data-integration
python scripts/client.py --help
```

### 3.2 数据存储管理-列表查询（iiot类型）

```bash
python scripts/client.py data-storage-list
python scripts/client.py data-storage-list --keyword 工作流
python scripts/client.py data-storage-list --tags 1
python scripts/client.py data-storage-list --page-no 1 --page-size 20
```

### 3.3 数据存储管理-获取表结构数据（iiot类型）

```bash
python scripts/client.py get-table-structure --table-id _plan_t_flow_instance
python scripts/client.py get-table-structure --table-id _plan_t_flow_instance --is-copy 1
```

### 3.4 系统-标签表-获取标签树（iiot类型）

```bash
python scripts/client.py get-tags-tree --type storage
```

### 3.5 数据存储管理-获取关联表数据（iiot类型）

```bash
python scripts/client.py get-refer-table-data --table-id m1120_device_status --page-no 1 --page-size 10
python scripts/client.py get-refer-table-data --table-id m1120_device_status \
  --field status --condition eq --value 1
```

### 3.6 数据存储管理-获取表字段信息（iiot类型）

```bash
python scripts/client.py table-field-list --table-id HZ_TESTaa --page-no 1 --page-size 10
python scripts/client.py table-field-list --table-id HZ_TESTaa --is-page 0
```

### 3.7 数据存储管理-查询所有表关系列表（faas类型）

```bash
python scripts/client.py get-table-relationship-list --page 1 --page-size 10
python scripts/client.py get-table-relationship-list \
  --main-table TEST__sys_t_role_data --foreign-table TEST_sys_role_permission
```

### 3.8 数据存储管理-获取关系详情接口（faas类型）

```bash
python scripts/client.py get-table-relationship-detail --id 11
```

---

## 四、返回格式

### iiot 类型成功

```json
{
  "success": true,
  "message": "",
  "code": 200,
  "result": {  },
  "timestamp": 1774935858801,
  "requestId": "..."
}
```

### faas 类型成功

```json
{
  "errorCode": 0,
  "errorMsg": "success",
  "times": "mySql总耗时 -> 0.123 秒。Redis总耗时 -> 0.005 秒。",
  "return": {  }
}
```

---

## 五、日志与调试

### 5.1 开启调试日志

默认日志级别为 INFO，如需查看请求详情，在 `scripts/client.py` 中修改：

```python
import logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(message)s")
```

### 5.2 常见错误码排查

| 错误码 | 说明       | 排查方法                           |
|-----|----------|--------------------------------|
| 401 | 认证失败     | 检查 SECRET_ID / SECRET_KEY 是否正确 |
| 408 | 请求超时     | 检查网络连通性或 API_URL 是否正确          |
| 502 | 响应非 JSON | 服务器异常，检查 API 服务状态              |
| 503 | 无法连接服务器  | 检查 API_URL 是否可达                |
| 404 | 命令未找到    | 检查命令拼写，可使用 `--help` 查看可用命令     |
| 500 | 未知错误     | 查看 errorMsg 详情，必要时开启 DEBUG 日志  |

---

## 六、测试

```bash
cd skills/ehz-iiot-data-integration
# 运行所有测试，生成测试报告
python scripts/test_client.py

# 运行所有测试，生成测试报告输出在test_report.txt
python scripts/test_client.py -o test_report.txt 2>&1

# 运行指定测试
python scripts/test_client.py test_data_storage_list

# 查看帮助
python scripts/test_client.py --help
```

---

## 七、快速参考

| 操作      | 命令                                                                 |
|---------|--------------------------------------------------------------------|
| 查看帮助    | `python scripts/client.py --help`                                  |
| 数据存储列表  | `python scripts/client.py data-storage-list`                       |
| 获取表结构   | `python scripts/client.py get-table-structure --table-id <ID>`     |
| 获取标签树   | `python scripts/client.py get-tags-tree --type storage`            |
| 获取关联表数据 | `python scripts/client.py get-refer-table-data --table-id <ID>`    |
| 获取表字段信息 | `python scripts/client.py table-field-list --table-id <ID>`        |
| 查询表关系列表 | `python scripts/client.py get-table-relationship-list`             |
| 获取关系详情  | `python scripts/client.py get-table-relationship-detail --id <ID>` |
| 运行测试    | `python scripts/test_client.py`                                    |
