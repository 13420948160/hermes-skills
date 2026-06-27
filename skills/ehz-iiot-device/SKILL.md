---
name: ehz-iiot-device
description: 极联平台设备接入相关技能，用于查询设备列表、设备数据、设备反控及实时数据获取。
version: "1.0.0"
author: "ehz"
license: MIT
metadata:
  hermes:
    tags: [iiot, device, iot]
    related_skills: []
---

# ehz-iiot-device 技能使用说明

封装极联平台设备管理 API，支持设备列表查询、属性数据获取、设备反控、实时数据批量获取。

## 一、环境配置

### 1.1 复制环境变量模板

```bash
cd skills/ehz-iiot-device
cp .env.example .env
```

### 1.2 编辑 `.env` 文件，填入实际值

| 变量名 | 说明 | 示例 |
|--------|------|------|
| API_URL | API 服务器地址 | your_api_url_here |
| ACCOUNT_ID | 极联平台账号 | your_account_id_here |
| SECRET_ID | 密钥ID | your_secret_id_here |
| SECRET_KEY | 密钥KEY | your_secret_key_here |
| TOKEN_VALID_SECONDS | Token 有效期（秒） | 900 |

> **提示**：如不创建 `.env` 文件，程序会自动读取系统环境变量，等效于已 export 所有变量。

**认证说明**：`TOKEN` 无需手动配置，客户端启动时会自动调用 `/ESBREST/faas/code/getAccessToken` 接口换取，token 有效期 15 分钟，客户端会自动刷新。

---

## 二、查询命令

### 2.1 查看所有可用命令

```bash
cd skills/ehz-iiot-device
python scripts/client.py --help
```

### 2.2 获取设备列表

```bash
# 默认（第一页，每页20条）
python scripts/client.py get-devices

# 按关键字模糊搜索（设备名称/SN/EID/设备编号）
python scripts/client.py get-devices --keyword 温度

# 筛选在线设备（1=在线，0=离线，-1=未接入）
python scripts/client.py get-devices --online 1

# 筛选有告警的设备
python scripts/client.py get-devices --alarm 1

# 组合筛选：关键字 + 在线 + 分页
python scripts/client.py get-devices --keyword 车间 --online 1 --page-index 1 --page-size 10
```

### 2.3 获取设备属性/测点数据

```bash
# 获取指定设备的测点数据列表
python scripts/client.py 获取设备属性数据 --eid IJJ2Q7IRQ8 --page-index 1 --page-size 20
```

### 2.4 获取设备实时数据（批量）

```bash
# 逗号分隔多个属性
python scripts/client.py get-real-time-data --attrs MOMTest.temperature,MOMTest.humidity,MOMTest.pressure
```

### 2.5 设备反控（写入数据）

```bash
# 格式：--attr {设备编号}.{属性ID} --value {值}
python scripts/client.py set-data --attr MOMTest.temperature --value 30
python scripts/client.py set-data --attr MOMTest.mode --value cooling
```

### 2.6 获取设备实时状态

```bash
# 批量获取设备实时状态（在线、告警数量、位置等）
python scripts/client.py get-equipment-rt-status --eids eid_001,eid_002,eid_003
```

### 2.7 根据标签获取设备列表

```bash
# 按标签ID查询（支持 keyword / online / alarm / emodelid 组合筛选）
python scripts/client.py get-devices-by-tag --tag-id tag_001 --keyword "" --page-index 1 --page-size 20

# 按标签分组ID查询
python scripts/client.py get-devices-by-tag --group-id group_001 --keyword "" --page-index 1 --page-size 20

# 组合筛选：只返回在线设备
python scripts/client.py get-devices-by-tag --tag-id tag_001 --online 1 --page-index 1 --page 10
```

### 2.8 获取告警历史数据

```bash
# 按分区查询告警历史（支持多条件筛选）
python scripts/client.py get-alarm-history --area-id area_001 --page-index 1 --page-size 20

# 筛选未清除的2级告警
python scripts/client.py get-alarm-history --area-id area_001 --status 1 --level 2 --page-index 1 --page-size 20

# 按设备+时间范围查询
python scripts/client.py get-alarm-history --area-id area_001 --eid eid_12345 \
  --start-time 2024-01-01T00:00:00.000Z --end-time 2024-01-31T23:59:59.000Z \
  --page-index 1 --page-size 20
```

### 2.9 获取设备历史数据

```bash
# 按设备EID查询历史数据（支持最多8个属性）
python scripts/client.py get-history-data \
  --eid eid_12345 --oids temperature,pressure \
  --start-time 2024-01-01T00:00:00.000Z \
  --end-time 2024-01-07T00:00:00.000Z \
  --interval 3600000 --page-index 1 --page-size 100

# 按设备编号+属性OID查询
python scripts/client.py get-history-data \
  --code MOMTest --oids MOMTest.temperature,MOMTest.humidity \
  --start-time 2024-01-01T00:00:00.000Z \
  --end-time 2024-01-07T00:00:00.000Z \
  --interval 3600000 --page-index 1 --page-size 100
```

### 调用流程

1. 配置环境变量（见上方）
2. 执行对应命令
3. 客户端自动调用 `/ESBREST/faas/code/getAccessToken` 获取 token（有效期 `TOKEN_VALID_SECONDS` 秒，过期自动刷新）
4. 返回 JSON 格式结果

### 返回格式

成功：
```json
{
  "errorCode": 0,
  "errorMsg": "操作成功",
  "return": { ... }
}
```

失败：
```json
{
  "errorCode": 401,
  "errorMsg": "认证失败：...",
  "return": null
}
```

---

## 三、查看特定命令的详细帮助

```bash
# 获取设备列表帮助
python scripts/client.py get-devices --help

# 设备反控帮助
python scripts/client.py set-data --help

# 实时数据帮助
python scripts/client.py get-real-time-data --help
```

---

## 四、日志与调试

### 4.1 开启调试日志

默认日志级别为 INFO，如需查看请求详情，在 `scripts/client.py` 中修改：

```python
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(message)s")
```

### 4.2 常见错误码排查

| 错误码 | 说明 | 排查方法 |
|--------|------|---------|
| 401 | 认证失败 | 检查 SECRET_ID / SECRET_KEY 是否正确 |
| 408 | 请求超时 | 检查网络连通性或 API_URL 是否正确 |
| 502 | 响应非 JSON | 服务器异常，检查 API 服务状态 |
| 503 | 无法连接服务器 | 检查 API_URL 是否可达 |
| 404 | 命令未找到 | 检查命令拼写，可使用 `--help` 查看可用命令 |
| 500 | 未知错误 | 查看 errorMsg 详情，必要时开启 DEBUG 日志 |

---

## 五、SKILL.md 文档生成

当 `references/api_docs.md` 更新后，需重新生成 `SKILL.md`：

```bash
cd skills/ehz-iiot-device
python scripts/generate_skill.py
```

指定自定义路径（不常用）：

```bash
python scripts/generate_skill.py \
  --api-docs references/api_docs.md \
  --output SKILL.md \
  --skill-name ehz-iiot-device
```

---

## 六、代码热更新流程（开发者）

当极联平台新增 API 接口时，只需：

1. **更新文档**：`references/api_docs.md` 按格式新增接口章节
2. **重新生成**：`python scripts/generate_skill.py` → 自动更新 `SKILL.md`
3. **验证命令**：`python scripts/client.py --help` → 新命令自动出现

无需修改任何 Python 代码。

---

## 七、快速参考

| 操作 | 命令 |
|------|------|
| 查看帮助 | `python scripts/client.py --help` |
| 设备列表 | `python scripts/client.py get-devices` |
| 设备列表（在线） | `python scripts/client.py get-devices --online 1` |
| 实时数据 | `python scripts/client.py get-real-time-data --attrs <属性1>,<属性2>` |
| 设备反控 | `python scripts/client.py set-data --attr <属性> --value <值>` |
| 设备实时状态 | `python scripts/client.py get-equipment-rt-status --eids <eid1>,<eid2>` |
| 按标签查设备 | `python scripts/client.py get-devices-by-tag --tag-id <ID> --keyword "" 
| 告警历史 | `python scripts/client.py get-alarm-history --area-id <ID> --page-index 1 --page-size 20` |
| 历史数据 | `python scripts/client.py get-history-data --eid <EID> --oids <属性1>,<属性2> --start-time <ISO> --end-time <ISO> --interval 3600000 --page-index 1 --page-size 100` |
| 重新生成文档 | `python scripts/generate_skill.py` |
