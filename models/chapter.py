



from sqlalchemy import Integer, String, DateTime, TEXT, func, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Chapter(Base):
    __tablename__ = "chapters"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)           
    course_id: Mapped[int] = mapped_column(Integer, index=True)                       
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(TEXT, nullable=True)
    video: Mapped[str] = mapped_column(String(255), nullable=True)
    rank: Mapped[int] = mapped_column(SmallInteger, server_default='1')  
    

    def to_dict(self):
        return {
            '编号': self.id,
            '章节编号': self.course_id,
            '章节标题': self.title,
            '章节内容': self.content,
            '章节视频': self.video,
            '排序': self.rank,
        }
        