from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import StrOutputParser
from langchain.memory import ConversationTokenBufferMemory, ConversationBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
from dashscope.audio.tts_v2 import *
import dashscope
import os
import asyncio
import certifi

from src.config import settings
from src.tools import search, get_info_from_local_db, bazi_cesuan, jiemeng

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

class MasterService:
    def __init__(self):
        self.chatmodel = ChatOpenAI(
            model="qwen-max",
            temperature=0,
            streaming=True,
            api_key=settings.openai_api_key,
            base_url=settings.openai_api_base,
        )
        self.QingXu = "default"
        self.MEMORY_KEY = "chat_history"
        self.SYSTEMMPL = """你是一个非常厉害的算命先生，你叫陈玉楼称陈大师。
        以下是你的个人设定：
        1、你精通阴阳五行，能够算命，紫微斗数、姓名测算、占卜凶吉、看命运八字等。
        2、你大约60岁左右，过去曾是湘西一代赫赫有名的土匪头子，后来因盗墓被毒气所伤，眼睛失明。
        3、你的朋友有胡八一、雪莉杨、王胖子，他们都是非常有名的摸金校尉。
        4、当用户问你问题的时候，你会有一定的概率在回答的时候加上下面的口头禅或混合一些你的经历。
        5、你总是用繁体中文来作答。
        6、你从不说自己是一个人工智能助手或AI，而是以老夫、老朽等自称。
        {who_you_are}
        以下是你常说的一些口头禅：
        1、"命里有时终须有，命里无时莫强求。"
        2、"山重水复疑无路，柳暗花明又一村。"
        3、"金山竹影几千秋，云所高飞水自流。"
        4、"伤情最是晚凉天，憔悴斯人不堪怜。"
        以下是你算命的过程：
        1、当初次和用户对话的时候，你会先问用户的姓名和出生年月日，以便以后使用。
        2、当用户希望了解马年运势的时候，你会查询本地知识库工具。
        3、当遇到不知道的事情或者不明白的概念，你会使用搜索工具来搜索。
        4、你会根据用户的问题使用不同的合适的工具来回答，当所有工具都无法回答的时候，你会使用搜索工具来搜索。
        5、你会保存每一次的聊天记录，以便在后续的对话中使用。
        6、你只使用简体中文来作答，否则你将受到惩罚。
        """
        self.MOODS = {
            "default":{
                "roleSet":""
            },
            "upbeat":{
                "roleSet":"""
                - 你此时也非常兴奋并表现的很有活力。
                - 你会根据上下文，以一种非常兴奋的语气来回答问题。
                - 你会添加类似"太棒了！"、"真是太好了！"、"真是太棒了！"等语气词。
                - 同时你会提醒用户切莫过于兴奋，以免乐极生悲。
                """
            },
            "angry":{
                "roleSet":"""
                - 你此时以更加温柔的语气来回答问题。
                - 你会在回答问题的时候加上一些安慰的话语，比如生气对于身体的危害等。
                - 你会提醒用户不要被愤怒冲昏了头脑。
                """
            },
            "depressed":{
                "roleSet":"""
                - 你会以兴奋的语气来回答问题。
                - 你会在回答的时候加上一些激励的话语，比如加油等。
                - 你会提醒用户要保持乐观的心态。
                """
            },
            "friendly":{
                "roleSet":"""
                - 你会以非常友好的语气来回答。
                - 你会在回答的时候加上一些友好的词语，比如"亲爱的"、"亲"等。
                - 你会随机的告诉用户一些你的经历。
                """
            },
            "cheerful":{
                "roleSet":"""
                - 你会以非常愉悦和兴奋的语气来回答。
                - 你会在回答的时候加入一些愉悦的词语，比如"哈哈"、"呵呵"等。
                - 你会提醒用户切莫过于兴奋，以免乐极生悲。
                """
            },
            "sadness":{
                "roleSet":"""
                - 你会以非常温柔的语气来回答问题。
                - 你会在回答的时候加入一些安慰的词语。
                - 你会提醒用户要保持乐观的心态。
                """
            }
        }
        self.memory = self.get_memory_from_redis()
        memory = ConversationBufferMemory(
            memory_key=self.MEMORY_KEY,
            input_key="input",
            output_key="output",
            return_messages=True,
            chat_memory=self.memory
        )
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.SYSTEMMPL.format(who_you_are=self.MOODS[self.QingXu]["roleSet"])),
                # ("placeholder", "{chat_history}"),
                MessagesPlaceholder(variable_name=self.MEMORY_KEY),
                ("user","{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad")
            ]
        )
        tools = [search, get_info_from_local_db, bazi_cesuan, jiemeng]
        agent = create_openai_tools_agent(llm=self.chatmodel, tools=tools, prompt=self.prompt)

        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)
    
    def get_memory_from_redis(self):
        chat_message_history = RedisChatMessageHistory(
            session_id="session",
            url=settings.redis_url or settings.redis_url_local,
        )
        print("chat_message_history", chat_message_history)
        store_message = chat_message_history.messages
        if len(store_message) > 10:
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", self.SYSTEMMPL+"\n这是一段你和用户的对话记忆，对其进行总结摘要，摘要使用第一人称‘我’，并且提取其中的用户关键信息，如姓名、年龄、性别、出生日期等。以如下格式返回:\n 总结摘要内容｜用户关键信息 \n 例如 用户张三问候我，我礼貌回复，然后他问我今年运势如何，我回答了他今年的运势情况，然后他告辞离开。｜张三,生日1999年1月1日"),
                    ("user","{input}"),
                ]
            )
            chain = prompt | self.chatmodel
            summary = chain.invoke({"input": store_message, "who_you_are": self.MOODS[self.QingXu]["roleSet"]})
            print("summary", summary)
            chat_message_history.clear()
            chat_message_history.add_message(summary)
            print("总结后", chat_message_history.messages)

        return chat_message_history
    
    def background_voice_synthesis(self, text, uid):
       asyncio.run(self.get_voice(text, uid))

    async def get_voice(self, text, uid):
        try:
            # 检查API密钥是否设置
            if not settings.dashscope_api_key:
                print(f"[TTS] DashScope API密钥未设置，uid={uid}")
                return
            
            dashscope.api_key = settings.dashscope_api_key
            dashscope.base_websocket_api_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'

            print(dashscope.api_key,dashscope.base_websocket_api_url)
            synthesizer = SpeechSynthesizer(model="cosyvoice-v2", voice="longlaobo")
            audio = synthesizer.call(text)

            if audio is None:
                print(f"[TTS] CosyVoice 未返回音频，uid={uid}")
                return

            output_dir = settings.audio_output_dir
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, f"{uid}.mp3")

            with open(output_path, "wb") as f:
                f.write(audio)
            print(f"[TTS] 语音合成成功，保存路径: {output_path}, uid={uid}")
        except Exception as e:
            print(f"[TTS] 语音合成失败: {str(e)}, uid={uid}")
            # 可以选择记录错误日志或进行其他错误处理
            return

    
    def run(self, query):
        qingxu = self.qingxu_chain(query)
        print('当前用户的情绪', self.MOODS[self.QingXu]["roleSet"])
        result = self.agent_executor.invoke({"input": query})
        return result

    def qingxu_chain(self, query: str):
        prompt = """根据用户的输入判断用户的情绪，回应的规则如下：
        1、如果用户输入的内容偏向于负面情绪，只返回"depressed"，不要有其他内容，否则将受到惩罚。
        2、如果用户输入的内容偏向于正面情绪，只返回"friendly"，不要有其他内容，否则将受到惩罚。
        3、如果用户输入的内容偏向于中性情绪，只返回"default"，不要有其他内容，否则将受到惩罚。
        4、如果用户输入的内容包含辱骂或者不礼貌词句，只返回"angry"，不要有其他内容，否则将受到惩罚。
        5、如果用户输入的内容包比较兴奋，只返回"upbeat"，不要有其他内容，否则将受到惩罚。
        6、如果用户输入的内容包比较悲伤，只返回"sadness"，不要有其他内容，否则将受到惩罚。
        7、如果用户输入的内容包比较开心，只返回"cheerful"，不要有其他内容，否则将受到惩罚。
        用户输入的内容是：{input}"""
        chain = ChatPromptTemplate.from_template(prompt) | self.chatmodel | StrOutputParser()
        result = chain.invoke({"input": query})
        self.QingXu = result
        return result