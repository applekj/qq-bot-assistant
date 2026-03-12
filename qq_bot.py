#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QQ 机器人实现
使用官方 botpy 库
"""
import certifi
import os
import sys
import logging
import ssl

# 加载 .env 文件
from dotenv import load_dotenv
load_dotenv()

# 设置 SSL 证书
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入依赖
import botpy
from botpy import logging
from botpy.message import Message
from src.services import MasterService

class MyClient(botpy.Client):
    async def on_at_message_create(self, message: Message):
        """处理被@的消息"""
        # 提取消息内容
        content = message.content.replace(f"<@!{self.robot.id}>", "").strip()
        
        if not content:
            await self.api.post_message(
                message.channel_id, 
                content="你好！我是陈玉楼，人称陈大师，有什么可以帮你的吗？"
            )
            return
        
        try:
            # 调用 AI Agent 服务
            master = MasterService()
            result = master.run(content)
            response = result.get("output", "抱歉，我暂时无法回答这个问题")
            
            # 发送文本消息
            await self.api.post_message(
                message.channel_id, 
                content=response
            )
        except Exception as e:
            logger.error(f"处理消息时出错: {e}")
            await self.api.post_message(
                message.channel_id, 
                content="处理消息时出错，请稍后再试"
            )

    async def on_c2c_message_create(self, message: Message):
        """处理私聊消息"""
        content = message.content.strip()
        print(f"收到私聊消息: {content}")
        
        if not content:
            await self.api.post_c2c_message(
                openid=message.author.user_openid,
                content="你好！我是 AI Agent 机器人，有什么可以帮你的吗？"
            )
            return
    
        try:
            # 调用 AI Agent 服务
            master = MasterService()
            result = master.run(content)
            response = result.get("output", "抱歉，我暂时无法回答这个问题")
            
            # 发送文本消息
            await self.api.post_c2c_message(
                openid=message.author.user_openid,
                content=response
            )
        except Exception as e:
            logger.error(f"处理私聊消息时出错: {e}")
            await self.api.post_c2c_message(
                openid=message.author.user_openid,
                content="处理消息时出错，请稍后再试"
            )

    async def on_ready(self):
        """机器人就绪"""
        logger.info(f"机器人 {self.robot.name} 已就绪")

if __name__ == "__main__":
    # 从环境变量读取配置
    appid = os.environ.get("QQ_BOT_APPID")
    secret = os.environ.get("QQ_BOT_APPSECRET")
    
    if not appid or not secret:
        logger.error("QQ 机器人配置缺失，请在 .env 文件中设置 QQ_BOT_APPID 和 QQ_BOT_APPSECRET")
        sys.exit(1)
    
    # 设置需要监听的事件
    intents = botpy.Intents(
        public_guild_messages=True,
        direct_message=True,
        public_messages=True
    )
    
    # 创建客户端
    client = MyClient(intents=intents)
    
    # 运行机器人
    try:
        client.run(appid=appid, secret=secret)
    except Exception as e:
        logger.error(f"机器人启动失败: {e}")
        sys.exit(1)
