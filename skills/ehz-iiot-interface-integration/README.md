# ehz-iiot-interface-integration

极联平台接口管理集成 CLI 工具，支持应用接入管理、接口服务列表查询、接口文档获取和接口调试调用。

## 快速开始

### 1. 环境配置

```bash
cd skills/ehz-iiot-interface-integration
cp .env.example .env
# 编辑 .env 填入 API_URL、ACCOUNT_ID、SECRET_ID、SECRET_KEY
```

### 2. 查看帮助

```bash
python scripts/client.py --help
```

### 3. 查看所有命令

```bash
python scripts/client.py app-list --help
python scripts/client.py app-interface-list --help
python scripts/client.py get-interface-doc --help
python scripts/client.py debug-app-interface --help
```

## API 类型

| 类型 | 前缀 | 请求方式 | 返回格式 |
|------|------|---------|---------|
| edge | `/ESBREST/edge/` | POST，参数直接传递 | `{errorCode, errorMsg, return}` |
| faas | `/ESBREST/faas/` | POST，参数包装在 `{apikey, request}` 中 | `{errorCode, errorMsg, return}` |
| iiot | `/ESBREST/iiot/` | GET/POST，参数直接传递 | `{success, code, message, result}` |

## 接口清单

| 接口 | 类型 | 说明 |
|------|------|------|
| `POST /ESBREST/edge/app/getAppList` | edge | 获取API管理应用接入列表 |
| `POST /ESBREST/edge/app/getAppInterfaceList` | edge | 根据标识符查询接口服务列表 |
| `POST /ESBREST/faas/code/get_interface_doc` | faas | 获取单个接口文档 |
| `POST /ESBREST/edge/app/debugAppInterface` | edge | 调用API管理接口服务 |

## 使用示例

### 应用接入列表

```bash
# 默认分页（第一页，每页10条）
python scripts/client.py app-list

# 关键字搜索
python scripts/client.py app-list --name 业务云函数

# 自定义分页
python scripts/client.py app-list --page 1 --size 20
```

### 接口服务列表

```bash
# 按应用ID查询
python scripts/client.py app-interface-list --app-id 3710e1d4-7a76-40d0-84a5-81224d3fe892

# 关键字搜索
python scripts/client.py app-interface-list --name insertProductionPlan

# 自定义分页
python scripts/client.py app-interface-list --app-id <UUID> --page 1 --size 20
```

### 获取接口文档

```bash
python scripts/client.py get-interface-doc \
  --addr insertProductionPlan \
  --app-name 业务云函数管理
```

### 调试接口服务

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

## 测试

```bash
# 运行所有测试
python scripts/test_client.py

# 输出报告到文件（文本 + JSON）
python scripts/test_client.py -o test_report.txt 2>&1

# 运行指定测试
python scripts/test_client.py app-list

# 列出所有测试用例
python scripts/test_client.py --list
```

**测试策略**：原子化独立测试，最多 10 次重试，连续 10 次失败直接退出。

## 返回格式

### edge/faas 类型成功

```json
{
  "errorCode": 0,
  "errorMsg": "执行成功！",
  "return": { ... }
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

## 常见错误

| 错误码 | 说明 | 排查方法 |
|--------|------|---------|
| 401 | 认证失败 | 检查 SECRET_ID / SECRET_KEY |
| 408 | 请求超时 | 检查网络或 API_URL |
| 502 | 响应非 JSON | 服务器异常 |
| 503 | 无法连接 | 检查 API_URL 可达性 |
| 500 | 未知错误 | 查看 errorMsg |
