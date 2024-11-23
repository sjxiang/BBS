from sqlalchemy import Integer, String, DateTime, TEXT, func, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Like(Base):
    """ 点赞 """
    
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(Integer, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True)    
    
    
    def to_dict(self):
        return {
            '编号': self.id,
            '课程编号': self.course_id,
            '用户编号': self.user_id,
        }
        