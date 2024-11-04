# DawnKeeper

DawnKeeper 是一个用于自动化连接 Dawn Network 浏览器扩展的 Python 脚本。它可以自动执行保活操作并监控积分情况。

## 功能特点

- 🔄 自动保活
- 💰 积分查询
- 👥 多账号支持
- 🌐 代理支持
- 🎨 彩色命令行界面
- ⏱️ 可配置的延迟时间

## 安装要求

- Python 3.7+
- pip (Python包管理器)

## 依赖安装

```bash
pip install requests python-dotenv colorama
```

## 配置说明

### 1. 创建配置文件

首先需要创建两个配置文件：`.env` 和 `accounts.json`

#### `.env` 文件
```ini
# 基本配置
USE_PROXY=false
MIN_DELAY=3
MAX_DELAY=10
RESTART_DELAY=241
ACCOUNT_DELAY=121
```

#### `accounts.json` 文件
```json
{
    "account1": {
        "email": "your_email@gmail.com",
        "token": "your_token_here",
        "proxy": ""
    },
    "account2": {
        "email": "another_email@gmail.com",
        "token": "another_token_here",
        "proxy": "http://proxy:port"
    }
}
```

### 2. 获取 Token 的详细步骤

1. 安装 Dawn Network 浏览器扩展
2. 登录你的账号
3. 按 F12 打开浏览器开发者工具
4. 切换到 "Network"（网络）标签页
5. 在扩展中执行任意操作（如点击刷新）
6. 在网络请求列表中找到 `updatename` 请求
7. 点击该请求，在右侧面板中找到 "Headers"（请求头）
8. 在请求头中找到 `Authorization` 字段
9. 复制该字段的值（注意：不要包含 "Bearer" 前缀）
10. 将复制的值粘贴到 `accounts.json` 中对应账号的 `token` 字段

### 3. 配置说明

#### 基本配置 (.env)
- `USE_PROXY`: 是否启用代理 (true/false)
- `MIN_DELAY`: 最小延迟时间（秒）
- `MAX_DELAY`: 最大延迟时间（秒）
- `RESTART_DELAY`: 完整循环后的重启延迟时间（秒）
- `ACCOUNT_DELAY`: 处理下一个账号前的延迟时间（秒）

#### 账号配置 (accounts.json)
- `email`: Dawn Network 账号邮箱
- `token`: 从浏览器获取的授权令牌（不包含 Bearer 前缀）
- `proxy`: 代理服务器地址（如不使用代理则留空）

## 使用方法

1. 克隆或下载项目
2. 安装所需依赖：
```bash
pip install requests python-dotenv colorama
```
3. 创建并配置 `.env` 和 `accounts.json` 文件
4. 运行脚本：
```bash
python main.py
```

## 代理配置示例

支持以下格式的代理配置：
```text
http://proxy:port
https://proxy:port
https://username:password@proxy:port
socks5://proxy:port
```

## 注意事项

- Token 安全：请妥善保管你的 token，不要泄露给他人
- 代理使用：如果启用代理但账号未配置代理，该账号会被跳过处理
- 延迟设置：建议根据实际情况调整延迟时间，避免请求过于频繁
- 网络要求：确保网络连接稳定，以保证脚本正常运行

## 常见问题

Q: 如何添加多个账号？  
A: 在 `accounts.json` 中添加新的账号配置即可，确保每个账号配置格式正确。

Q: 运行时出现 SSL 错误怎么办？  
A: 脚本已默认处理了 SSL 证书验证问题，如果仍有问题，请检查网络连接。

Q: 代理不工作怎么办？  
A: 检查以下几点：
1. `.env` 中的 `USE_PROXY` 是否设置为 true
2. 代理地址格式是否正确
3. 代理服务器是否可用
