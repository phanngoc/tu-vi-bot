"""
Database Manager Component

Component quản lý database và session, có thể dễ dàng thay thế bằng các database khác.
"""

import json
import sqlite3
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from datetime import datetime

from .interfaces import IDatabaseManager, ConversationContext, ConversationState, UserInfo
from models import UserSession, ChatHistory, Session as DBSession


class DatabaseManager(IDatabaseManager):
    """Quản lý database và session"""
    
    def __init__(self, db_path: str = "tuvi.db"):
        self.db_path = db_path
        self._ensure_database_integrity()
    
    def save_user_session(self, user_id: str, context: ConversationContext) -> None:
        """Lưu session người dùng"""
        with self._get_db_session() as db_session:
            session_record = db_session.query(UserSession).filter(
                UserSession.session_id == user_id
            ).first()
            
            if not session_record:
                session_record = UserSession(
                    session_id=user_id,
                    current_step=context.state.value,
                    collected_info=json.dumps(self._user_info_to_dict(context.collected_info)),
                    memory_summary=""
                )
                db_session.add(session_record)
            else:
                session_record.current_step = context.state.value
                session_record.collected_info = json.dumps(self._user_info_to_dict(context.collected_info))
                session_record.updated_at = datetime.utcnow()
            
            db_session.commit()
    
    def get_user_session(self, user_id: str) -> Optional[ConversationContext]:
        """Lấy session người dùng"""
        with self._get_db_session() as db_session:
            session_record = db_session.query(UserSession).filter(
                UserSession.session_id == user_id
            ).first()
            
            if not session_record:
                return None
            
            # Parse collected info
            collected_info_dict = json.loads(session_record.collected_info or '{}')
            collected_info = UserInfo(
                name=collected_info_dict.get('name', ''),
                birthday=collected_info_dict.get('birthday', ''),
                birth_time=collected_info_dict.get('birth_time', ''),
                gender=collected_info_dict.get('gender', '')
            )
            
            # Get message history
            message_history = self.get_chat_history(user_id, limit=10)
            
            return ConversationContext(
                user_id=user_id,
                state=ConversationState(session_record.current_step),
                collected_info=collected_info,
                message_history=message_history
            )
    
    def save_chat_message(self, user_id: str, message: str, role: str) -> None:
        """Lưu tin nhắn chat"""
        with self._get_db_session() as db_session:
            chat_record = ChatHistory(
                user_id=user_id,
                message=message,
                role=role,
                step="",  # Có thể thêm step nếu cần
                extracted_info=None
            )
            db_session.add(chat_record)
            db_session.commit()
    
    def get_chat_history(self, user_id: str, limit: int = 50) -> List[Dict[str, str]]:
        """Lấy lịch sử chat"""
        with self._get_db_session() as db_session:
            history = db_session.query(ChatHistory).filter(
                ChatHistory.user_id == user_id
            ).order_by(ChatHistory.created_at.desc()).limit(limit).all()
            
            return [{
                'message': h.message,
                'role': h.role,
                'step': h.step or '',
                'created_at': h.created_at.isoformat() if h.created_at else ''
            } for h in reversed(history)]
    
    def reset_user_session(self, user_id: str) -> None:
        """Reset session người dùng"""
        with self._get_db_session() as db_session:
            # Reset session
            session_record = db_session.query(UserSession).filter(
                UserSession.session_id == user_id
            ).first()
            
            if session_record:
                session_record.current_step = ConversationState.GREETING.value
                session_record.collected_info = json.dumps({})
                session_record.memory_summary = ""
                session_record.updated_at = datetime.utcnow()
            
            # Clear chat history
            db_session.query(ChatHistory).filter(
                ChatHistory.user_id == user_id
            ).delete()
            
            db_session.commit()
    
    def _get_db_session(self):
        """Context manager cho database session"""
        session = DBSession()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Database error: {e}")
            # Try to recreate database if corrupted
            if "malformed" in str(e).lower() or "corrupted" in str(e).lower():
                print("Database appears corrupted, attempting to recreate...")
                self._recreate_database()
            raise e
        finally:
            session.close()
    
    def _ensure_database_integrity(self) -> None:
        """Đảm bảo tính toàn vẹn database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check;")
            result = cursor.fetchone()
            conn.close()
            
            if result[0] != 'ok':
                print(f"Database integrity check failed: {result[0]}")
                self._recreate_database()
        except Exception as e:
            print(f"Error checking database integrity: {e}")
            self._recreate_database()
    
    def _recreate_database(self) -> None:
        """Tạo lại database từ đầu"""
        try:
            from models import Base, engine
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            print("Database recreated successfully")
        except Exception as e:
            print(f"Failed to recreate database: {e}")
            raise e
    
    def _user_info_to_dict(self, user_info: UserInfo) -> Dict[str, str]:
        """Convert UserInfo to dictionary"""
        return {
            'name': user_info.name,
            'birthday': user_info.birthday,
            'birth_time': user_info.birth_time,
            'gender': user_info.gender
        }
