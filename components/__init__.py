"""
Tu Vi Bot Components Package

Kiến trúc component-based cho hệ thống tư vấn tử vi thông minh.
Mỗi component có thể được thay thế độc lập mà không ảnh hưởng đến các component khác.
"""

from .interfaces import (
    ITuviCalculator,
    IConversationManager, 
    IDatabaseManager,
    IInformationExtractor,
    IResponseGenerator,
    ILLMProvider
)

from .tuvi_calculator import TuviCalculator
from .conversation_manager import ConversationManager
from .database_manager import DatabaseManager
from .information_extractor import InformationExtractor
from .response_generator import ResponseGenerator
from .llm_provider import LLMProvider

__all__ = [
    'ITuviCalculator',
    'IConversationManager',
    'IDatabaseManager', 
    'IInformationExtractor',
    'IResponseGenerator',
    'ILLMProvider',
    'TuviCalculator',
    'ConversationManager',
    'DatabaseManager',
    'InformationExtractor', 
    'ResponseGenerator',
    'LLMProvider'
]
