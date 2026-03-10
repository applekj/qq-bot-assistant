import pytest
from src.services import MasterService


@pytest.fixture
def master_service():
    return MasterService()


def test_master_service_initialization(master_service):
    """测试MasterService初始化是否成功"""
    assert master_service is not None
    assert master_service.chatmodel is not None
    assert master_service.agent_executor is not None


def test_qingxu_chain(master_service):
    """测试情绪分析链"""
    test_queries = [
        ("你好，很高兴认识你", "friendly"),
        ("今天天气真差，心情很不好", "depressed"),
        ("请问今天是星期几", "default"),
    ]
    
    for query, expected in test_queries:
        result = master_service.qingxu_chain(query)
        assert result in ["friendly", "depressed", "default", "angry", "upbeat", "sadness", "cheerful"]


def test_run_method(master_service):
    """测试run方法是否能正常执行"""
    test_query = "你好，请问你是谁？"
    result = master_service.run(test_query)
    assert "output" in result
    assert isinstance(result["output"], str)
