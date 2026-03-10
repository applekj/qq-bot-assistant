import pytest
from src.tools import search, get_info_from_local_db, bazi_cesuan, jiemeng


def test_search_tool():
    """测试搜索工具"""
    test_query = "今天天气如何"
    result = search(test_query)
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_info_from_local_db():
    """测试本地数据库查询工具"""
    test_query = "2026年运势"
    result = get_info_from_local_db(test_query)
    assert isinstance(result, list)


def test_bazi_cesuan():
    """测试八字测算工具"""
    test_query = "张三，1990年1月1日8点出生"
    result = bazi_cesuan(test_query)
    assert isinstance(result, str)


def test_jiemeng():
    """测试解梦工具"""
    test_query = "我梦见自己在飞"
    result = jiemeng(test_query)
    assert isinstance(result, (str, dict))
