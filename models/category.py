from sqlalchemy import Integer, String, DateTime, TEXT, func, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

from database import connect_db

# 连接数据库
db = connect_db()


class Category(Base):
    """ 分类 """
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
    
    
    @staticmethod
    def add_category(name: str, rank: int) -> dict | None:
        """ 添加 """

        category = db.query(Category).filter(Category.name == name).one_or_none()
        
        if category:
           return None 
    
        new_category = Category(name=name, rank=rank)

        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return new_category.to_dict()


    @staticmethod
    def query_all() -> list:
        """ 查询所有 """

        result = db.query(Category).order_by(Category.rank.asc()).all()

        items = []

        for e in result:
            items.append(e.to_dict())

        return items