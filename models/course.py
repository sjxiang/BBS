from sqlalchemy import Integer, String, DateTime, TEXT, func, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Course(Base):
    __tablename__ = "courses"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)           
    category_id: Mapped[int] = mapped_column(Integer)  
    name: Mapped[str] = mapped_column(String(255))                       
 
    
    def to_dict(self):
        return {
            '编号': self.id,
            '分类名称': self.name,
            '排序': self.rank,
        }
    