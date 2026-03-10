#!/bin/bash

# 构建项目
echo "Building project..."

# 检查依赖
echo "Checking dependencies..."
pip check

# 运行测试
echo "Running tests..."
pytest tests/

echo "Build completed successfully!"