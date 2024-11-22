from sqlalchemy import Integer, String, DateTime, func, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, Session
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nickname: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    avatar: Mapped[str] = mapped_column(String(1024))
    is_admin: Mapped[int] = mapped_column(SmallInteger, server_default='0')  # 0 表示普通用户, 1 表示管理员
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # 小贴士, sqlalchemy 2.0 用法, 字段默认 NOT NULL
    

    def to_dict(self):
        return {
            '编号': self.id,
            '昵称': self.nickname,
            '邮件': self.email,
            '头像': self.avatar,
            '管理员': self.is_admin == 0,
            '创建时间': self.created_at,
            '更新时间': self.updated_at,
        }