from sqlalchemy import Integer, String, DateTime, TEXT, func, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from database import Base

        
class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))                          
    content: Mapped[str] = mapped_column(TEXT)                               
    user_id: Mapped[int] = mapped_column(Integer)                            
    is_draft: Mapped[int] = mapped_column(SmallInteger, server_default='1')  
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    
    def to_dict(self):
        return {
            '编号': self.id,
            '标题': self.title,
            '内容': self.content,
            '作者': self.user_id,
            '草稿': self.is_draft == 1,
            '创建时间': self.created_at,
            '更新时间': self.updated_at,
        }
        
    
