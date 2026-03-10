#!/bin/bash

# 环境变量配置脚本
echo "Setting up environment variables..."

# 检查.env文件是否存在
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << EOF
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
EOF
    echo ".env file created. Please update the API keys."
else
    echo ".env file already exists."
fi