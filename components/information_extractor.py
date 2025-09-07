"""
Information Extractor Component

Component trích xuất thông tin từ tin nhắn người dùng, có thể dễ dàng thay thế bằng các phương pháp khác.
"""

import re
from typing import List, Optional
from datetime import datetime, date, time

from .interfaces import IInformationExtractor, UserInfo, ConversationContext


class InformationExtractor(IInformationExtractor):
    """Trích xuất thông tin từ tin nhắn người dùng sử dụng LLM"""
    
    def __init__(self, llm_provider=None):
        self.llm_provider = llm_provider
    
    def extract_user_info(self, message: str, context: ConversationContext) -> UserInfo:
        """Trích xuất thông tin người dùng từ tin nhắn sử dụng LLM"""
        if not self.llm_provider:
            # Fallback: return existing info if no LLM provider
            return context.collected_info
        
        # Use LLM to extract information
        extracted_info = self.llm_provider.extract_information(message, context)
        
        # If we have complete information, save to database
        if self.is_info_complete(extracted_info):
            self._save_user_to_database(extracted_info, context.user_id)
        
        return extracted_info
    
    def _save_user_to_database(self, user_info: UserInfo, user_id: str):
        """Lưu thông tin người dùng vào database"""
        try:
            from models import User, Session
            
            # Parse date and time
            birth_date = None
            birth_hour = None
            
            if user_info.birthday:
                try:
                    birth_date = datetime.strptime(user_info.birthday, "%d/%m/%Y").date()
                except ValueError:
                    pass
            
            if user_info.birth_time:
                try:
                    birth_hour = datetime.strptime(user_info.birth_time, "%H:%M").time()
                except ValueError:
                    pass
            
            # Create database session
            db_session = Session()
            
            try:
                # Check if user already exists
                existing_user = db_session.query(User).filter(User.name == user_info.name).first()
                
                if existing_user:
                    # Update existing user
                    existing_user.birth_date = birth_date
                    existing_user.birth_hour = birth_hour
                    existing_user.gender = user_info.gender
                    print(f"✅ Updated user in database: {user_info.name}")
                else:
                    # Create new user
                    new_user = User(
                        name=user_info.name,
                        birth_date=birth_date,
                        birth_hour=birth_hour,
                        gender=user_info.gender
                    )
                    db_session.add(new_user)
                    print(f"✅ Saved new user to database: {user_info.name}")
                
                db_session.commit()
                
            except Exception as e:
                db_session.rollback()
                print(f"❌ Error saving user to database: {e}")
            finally:
                db_session.close()
                
        except ImportError:
            print("⚠️ Models not available, skipping database save")
        except Exception as e:
            print(f"❌ Error accessing database: {e}")
    
    def is_info_complete(self, user_info: UserInfo) -> bool:
        """Kiểm tra xem đã có đủ thông tin chưa"""
        return all([
            user_info.name.strip(),
            user_info.birthday.strip(),
            user_info.birth_time.strip(),
            user_info.gender.strip()
        ])
    
    def get_missing_fields(self, user_info: UserInfo) -> List[str]:
        """Lấy danh sách thông tin còn thiếu"""
        missing = []
        
        if not user_info.name.strip():
            missing.append('tên')
        
        if not user_info.birthday.strip():
            missing.append('ngày sinh')
        
        if not user_info.birth_time.strip():
            missing.append('giờ sinh')
        
        if not user_info.gender.strip():
            missing.append('giới tính')
        
        return missing


