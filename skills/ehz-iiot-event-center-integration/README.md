# ehz-iiot-event-center-integration

极联平台事件中心集成 CLI 工具，支持事件中心申明管理和动作管理。

## 快速开始

### 1. 环境配置

```bash
cd skills/ehz-iiot-event-center-integration
cp .env.example .env
# 编辑 .env 填入 API_URL、ACCOUNT_ID、SECRET_ID、SECRET_KEY
```

### 2. 查看帮助

```bash
python scripts/client.py --help
```

### 3. 查看所有命令

```bash
python scripts/client.py event-define-list --help
python scripts/client.py event-action-list --help
python scripts/client.py send-to-event-message --help
```

## API 类型

| 类型 | 前缀 | 请求方式 | 返回格式 |
|------|------|---------|---------|
| iiot | `/ESBREST/iiot/` | GET/POST，参数直接传递 | `{success, code, message, result}` |
| faas | `/ESBREST/faas/` | POST，参数包装在 `{apikey, request}` 中 | `{errorCode, errorMsg, return}` |

## 接口清单

| 接口 | 类型 | 说明 |
|------|------|------|
| `GET /ESBREST/iiot/event/EventDefine/list` | iiot | 事件中心申明表-分页列表 |
| `GET /ESBREST/iiot/event/eventAction/list` | iiot | 事件中心动作表-分页列表 |
| `GET /ESBREST/iiot/event/EventDefine/listAll` | iiot | 事件中心申明表-导出（不分页） |
| `POST /ESBREST/faas/coode/sendToEventMessage` | faas | 发布事件消息到队列 |

## 使用示例

### 事件中心申明列表

```bash
# 默认分页（第一页，每页10条）
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

### 事件中心动作列表

```bash
# 默认分页
python scripts/client.py event-action-list

# 按动作名称搜索
python scripts/client.py event-action-list --action-name 测试

# 按状态筛选
python scripts/client.py event-action-list --action-status 1

# 自定义分页
python scripts/client.py event-action-list --page-no 1 --page-size 20
```

### 导出所有事件中心申明

```bash
# 导出所有记录
python scripts/client.py event-define-export-all

# 按名称筛选导出
python scripts/client.py event-define-export-all --name 测试

# 按状态筛选导出
python scripts/client.py event-define-export-all --status 1
```

### 发布事件消息（faas 类型）

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

## 测试

```bash
# 运行所有测试
python scripts/test_client.py

# 输出报告到文件
python scripts/test_client.py -o test_report.txt 2>&1

# 运行指定测试
python scripts/test_client.py event_define_list

# 列出所有测试用例
python scripts/test_client.py --list
```

## 返回格式

### iiot 类型成功

```json
{
  "success": true,
  "message": "",
  "code": 200,
  "result": { ... },
  "timestamp": 1775025131933,
  "requestId": "8a49804a9d454a98019d47be119d16cf"
}
```

### faas 类型成功

```json
{
  "errorCode": 0,
  "errorMsg": "发布事件消息...",
  "return": {}
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
