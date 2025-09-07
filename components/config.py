"""
Configuration for Tu Vi Bot Components

Cấu hình tập trung cho tất cả các component.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Cấu hình database"""
    db_path: str = "tuvi.db"
    pool_size: int = 5
    pool_recycle: int = 300
    echo: bool = False


@dataclass
class LLMConfig:
    """Cấu hình LLM"""
    provider: str = "openai"  # openai, anthropic, mock
    model: str = "gpt-4o-mini"
    api_key: Optional[str] = None
    max_tokens: int = 2000
    temperature: float = 0.7


@dataclass
class TuViConfig:
    """Cấu hình Tu Vi Calculator"""
    use_lunar_calendar: bool = True
    enable_star_strength: bool = True
    enable_fortune_analysis: bool = True
    enable_guidance_recommendations: bool = True


@dataclass
class ConversationConfig:
    """Cấu hình Conversation Manager"""
    use_intelligent_mode: bool = True
    max_history_length: int = 50
    enable_memory_summary: bool = True
    auto_reset_after_hours: int = 24


@dataclass
class BotConfig:
    """Cấu hình tổng thể cho bot"""
    database: DatabaseConfig
    llm: LLMConfig
    tuvi: TuViConfig
    conversation: ConversationConfig
    
    @classmethod
    def from_env(cls) -> 'BotConfig':
        """Tạo config từ environment variables"""
        return cls(
            database=DatabaseConfig(
                db_path=os.getenv('TUVIBOT_DB_PATH', 'tuvi.db'),
                pool_size=int(os.getenv('TUVIBOT_DB_POOL_SIZE', '5')),
                pool_recycle=int(os.getenv('TUVIBOT_DB_POOL_RECYCLE', '300')),
                echo=os.getenv('TUVIBOT_DB_ECHO', 'false').lower() == 'true'
            ),
            llm=LLMConfig(
                provider=os.getenv('TUVIBOT_LLM_PROVIDER', 'openai'),
                model=os.getenv('TUVIBOT_LLM_MODEL', 'gpt-4o-mini'),
                api_key=os.getenv('TUVIBOT_LLM_API_KEY'),
                max_tokens=int(os.getenv('TUVIBOT_LLM_MAX_TOKENS', '2000')),
                temperature=float(os.getenv('TUVIBOT_LLM_TEMPERATURE', '0.7'))
            ),
            tuvi=TuViConfig(
                use_lunar_calendar=os.getenv('TUVIBOT_USE_LUNAR', 'true').lower() == 'true',
                enable_star_strength=os.getenv('TUVIBOT_ENABLE_STAR_STRENGTH', 'true').lower() == 'true',
                enable_fortune_analysis=os.getenv('TUVIBOT_ENABLE_FORTUNE_ANALYSIS', 'true').lower() == 'true',
                enable_guidance_recommendations=os.getenv('TUVIBOT_ENABLE_GUIDANCE', 'true').lower() == 'true'
            ),
            conversation=ConversationConfig(
                use_intelligent_mode=os.getenv('TUVIBOT_INTELLIGENT_MODE', 'true').lower() == 'true',
                max_history_length=int(os.getenv('TUVIBOT_MAX_HISTORY', '50')),
                enable_memory_summary=os.getenv('TUVIBOT_ENABLE_MEMORY', 'true').lower() == 'true',
                auto_reset_after_hours=int(os.getenv('TUVIBOT_AUTO_RESET_HOURS', '24'))
            )
        )
    
    @classmethod
    def default(cls) -> 'BotConfig':
        """Tạo config mặc định"""
        return cls(
            database=DatabaseConfig(),
            llm=LLMConfig(),
            tuvi=TuViConfig(),
            conversation=ConversationConfig()
        )


# Global config instance
_config: Optional[BotConfig] = None


def get_config() -> BotConfig:
    """Lấy config hiện tại"""
    global _config
    if _config is None:
        _config = BotConfig.from_env()
    return _config


def set_config(config: BotConfig):
    """Set config mới"""
    global _config
    _config = config


def reset_config():
    """Reset config về mặc định"""
    global _config
    _config = None
