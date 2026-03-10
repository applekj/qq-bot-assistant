from fastapi import APIRouter
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings.dashscope import DashScopeEmbeddings

from src.config import settings

router = APIRouter()


@router.get("/")
def read_root():
    return {"message": "Hello, World!"}


@router.post("/add_usls")
def add_url(url: str):   
    loader = WebBaseLoader(url)
    docs = loader.load()
    documents = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50).split_documents(docs)
    print("文档的数量", len(documents))
    
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v1",
        dashscope_api_key=settings.dashscope_api_key
    )
    
    qdrant = Qdrant.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=settings.qdrant_collection,
        path=settings.qdrant_path
    )
    print("向量数据库创建完成")
    print("qdrant", qdrant.collection_name)
    return {"url": url}