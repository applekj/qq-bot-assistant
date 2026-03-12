# AI Agent 项目

## 项目介绍

这是一个基于 FastAPI 和 LangChain 构建的 AI Agent 项目，主要功能包括：

- 智能聊天功能，支持多种工具调用
- 八字测算功能
- 解梦功能
- 本地知识库查询
- 实时搜索功能
- 语音合成功能
- QQ 机器人集成，支持群聊和私聊

## 项目结构

```
qq-bot-assistant/
├── src/
│   ├── api/           # API 路由
│   ├── config/        # 配置管理
│   ├── services/      # 业务逻辑
│   ├── tools/         # 工具函数
├── scripts/           # 运行脚本
├── tests/             # 测试代码
├── local_qdrant/      # 本地向量数据库
├── audio_output/      # 音频输出目录
├── Dockerfile         # Docker 配置
├── Docker-compose.yml # Docker Compose 配置
├── requirements.txt   # 依赖管理
├── server.py          # 应用入口
├── qq_bot.py          # QQ 机器人实现
└── README.md          # 项目文档
```

## 安装与运行

### 环境要求

- Python 3.10+
- Redis 7.0+
- Docker (可选)

### 本地安装

1. 克隆项目

2. 安装依赖
   ```bash
   ./scripts/install.sh
   ```

3. 配置环境变量
   ```bash
   ./scripts/env.sh
   ```
   然后编辑 `.env` 文件，填写以下内容：
   ```
   # OpenAI 配置
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_API_BASE=your_openai_api_base

   # 其他 API 配置
   SERPAPI_API_KEY=your_serpapi_api_key
   DASHSCOPE_API_KEY=your_dashscope_api_key
   YUANFENJU_API_KEY=your_yuanfenju_api_key

   # 数据库配置
   REDIS_URL=
   REDIS_URL_LOCAL=redis://localhost:6379/0

   # QQ 机器人配置
   QQ_BOT_APPID=your_qq_bot_appid
   QQ_BOT_APPSECRET=your_qq_bot_appsecret
   ```

4. 启动 Redis
   ```bash
   redis-server
   ```

5. 运行应用
   ```bash
   # 启动 AI 服务器
   ./scripts/start.sh
   
   # 运行 QQ 机器人（在另一个终端）
   python qq_bot.py
   ```

### Docker 运行

1. 配置环境变量
   创建 `.env` 文件，填写相关配置，包括 QQ 机器人配置

2. 启动服务
   ```bash
   # 启动所有服务（ai-server、redis-server、qq-bot）
   docker-compose up --build
   
   # 仅启动 QQ 机器人服务
   docker-compose up --build qq-bot
   ```

## API 接口

### 1. 聊天接口
- **URL**: `/chat/`
- **方法**: POST
- **参数**: `query` (字符串)
- **返回**: 聊天结果和音频文件ID

### 2. 添加 URL 到知识库
- **URL**: `/add_usls`
- **方法**: POST
- **参数**: `url` (字符串)
- **返回**: 添加结果

### 3. WebSocket 接口
- **URL**: `/ws`
- **方法**: WebSocket
- **功能**: 实时通信

## 功能说明

1. **智能聊天**: 基于 LangChain 和 OpenAI 模型，支持多种工具调用
2. **八字测算**: 通过 API 调用进行八字排盘
3. **解梦**: 通过 API 调用解析梦境含义
4. **本地知识库**: 使用 Qdrant 向量数据库存储和查询本地文档
5. **实时搜索**: 使用 SerpAPI 进行实时信息搜索
6. **语音合成**: 使用 DashScope 进行语音合成
7. **QQ 机器人**: 集成 QQ 官方 botpy 库，支持群聊@消息和私聊消息处理

## 技术栈

- FastAPI: Web 框架
- LangChain: LLM 应用框架
- OpenAI: 语言模型
- Qdrant: 向量数据库
- Redis: 缓存和会话管理
- DashScope: 语音合成
- botpy: QQ 机器人官方 SDK
- Docker: 容器化部署

## 测试

运行测试：
```bash
./scripts/test.sh
```

## 脚本说明

项目提供了以下脚本，位于 `scripts/` 目录：

- `start.sh` - 启动开发服务器
- `build.sh` - 构建项目（检查依赖和运行测试）
- `test.sh` - 运行测试
- `install.sh` - 安装依赖
- `env.sh` - 配置环境变量（创建.env文件）

使用方法：
```bash
./scripts/<脚本名称>.sh
```
