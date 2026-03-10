from langchain.agents import tool
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
from qdrant_client import QdrantClient
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
import requests
import json

YUANFENJU_API_KEY="7xdPvXsvZRq44PW1fO8qk6eRi"

@tool
def search(query:str):
    """只有需要了解实时信息或不知道的事情的时候才会调用这个工具"""
    serp = SerpAPIWrapper()
    result = serp.run(query)
    print("实时搜索结果：",result)
    return result

# 该方法未测试
@tool
def get_info_from_local_db(query:str):
    """只有需要了解2026年运势或马年运势的时候,才会使用这个工具"""
    print("使用本地数据")
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v2",  # 或 text-embedding-v3
    )

    client = Qdrant(
        client=QdrantClient(path="./local_qdrant"),
        collection_name="local_documents",
        embeddings=embeddings
    )

    retriever = client.as_retriever(search_type='mmr')
    result = retriever.get_relevant_documents(query)
    # result = retriever.invoke(query)
    print("本地数据库搜索结果：",result)
    return result

@tool
def bazi_cesuan(query:str):
    """只有做八字排盘的时候才会使用这个工具，需要输入用户姓名和出生年月日时，如果缺少用户姓名和出生年月日时则不可用。"""
    url = f"https://api.yuanfenju.com/index.php/v1/Bazi/cesuan"
    prompt = ChatPromptTemplate.from_template(
        """你是是一个参数查询助手，根据用户输入内容找出相关的参数并按json格式返回。JSON字段如下：
        -"api_key":"{api_key}",
        -"name":"姓名",
        -"sex":"性别，0表示难，1表示女，根据姓名判断",
        -"type":"日历类型，0农历，1公历，默认1",
        -"year":"出生年份 例：1988",
        -"month":"出生月份 例：8",
        -"day":"出生日期 例：8",
        -"hours":"出生小时 例：8",
        -"minute":"出生分钟 例：8",
        如果没有找到相关参数，则需要提醒用户告诉你这些内容，只返回数据结构，不要有其他的评论，用户输入：{query}"""
    )
    parser = JsonOutputParser()
    prompt = prompt.partial(format_instructions=parser.get_format_instructions(),api_key=YUANFENJU_API_KEY)
    chain = prompt | ChatOpenAI(model="qwen-max",
            temperature=0,
            streaming=True,) | parser
    data = chain.invoke({"query":query})
    print("八字测算",data)
    result = requests.post(url,data=data)
    if result.status_code == 200:
        print("====返回数据====")
        print(result.json())
        try:
            json = result.json()
            returnstring = f"八字为:{json['data']['bazi_info']['bazi']}"
            return returnstring
        except Exception as e:
            return "八字查询失败，可以是你忘记询问用户姓名或者出生年月日时了。"
    else:
        return "技术错误，请告诉用户稍后再试。"

@tool
def jiemeng(query:str):
    """
    解梦工具 - 当用户询问梦境含义时使用
    触发词：梦见，做梦，梦境，解梦，梦到，昨晚梦，梦里
    需要：用户描述梦境内容
    """
    api_key = YUANFENJU_API_KEY
    url = f"https://api.yuanfenju.com/index.php/v1/Gongju/zhougong"
    LLM = ChatOpenAI(model="qwen-max",
            temperature=0,)   
    prompt = PromptTemplate.from_template(
        "根据用户梦境内容提取一个关键词，只返回关键词，内容为:{topic}"
    )    
    prompt_value=prompt.invoke({"topic":query})
    keyword = LLM.invoke(prompt_value)
    # chain = ChatPromptTemplate.from_template(
    # "根据内容提取1个关键词，只返回关键词，内容为:{topic}"
    # ) | ChatOpenAI(model="qwen-plus", temperature=0, streaming=True)
    # keyword = chain.invoke({"topic": query})
    print("解梦关键词：",keyword.content)
    result = requests.post(url,data={"api_key":api_key,"title_zhougong":keyword.content})
    if result.status_code == 200:
        print("====返回数据====")
        print(result.json())
        try:
            returnstring = json.loads(result.text)
            return returnstring
        except Exception as e:
            return "解梦失败，请告诉用户稍后再试。"
    else:
        return "技术错误，请告诉用户稍后再试。"
   