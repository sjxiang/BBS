from sqlalchemy import Integer, String, DateTime, TEXT, func, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Course(Base):
    __tablename__ = "courses"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)           
    category_id: Mapped[int] = mapped_column(Integer, index=True)  
    name: Mapped[str] = mapped_column(String(255))                       
    user_id: Mapped[int] = mapped_column(Integer, index=True)
    image: Mapped[str] = mapped_column(String(255), nullable=True)
    recommended: Mapped[int] = mapped_column(SmallInteger, nullable=True, server_default='0', index=True)
    introductory: Mapped[int] = mapped_column(SmallInteger, nullable=True, server_default='0', index=True)
    content: Mapped[str] = mapped_column(TEXT, nullable=True)
    likes_count: Mapped[int] = mapped_column(Integer, server_default='0')
    chapters_count: Mapped[int] = mapped_column(Integer, server_default='0')
    
    
    def to_dict(self):
        return {
            '编号': self.id,
            '分类编号': self.category_id,
            '课程名称': self.name,
            '用户编号': self.user_id,
            '课程图片': self.image,
            '是否推荐': self.recommended,
            '是否为入门课程': self.introductory,
            '课程内容': self.content,
            '课程的点赞数': self.likes_count,
            '课程的章节数量': self.chapters_count,
        }