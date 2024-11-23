from sqlalchemy import Integer, String, DateTime, TEXT, func, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


# 课程分类

class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)           
    name: Mapped[str] = mapped_column(String(255), unique=True)                       
    rank: Mapped[int] = mapped_column(SmallInteger, server_default='1')  
    
    
    def to_dict(self):
        return {
            '编号': self.id,
            '分类名称': self.name,
            '排序': self.rank,
        }
    