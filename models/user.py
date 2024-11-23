from sqlalchemy import Integer, String, DateTime, func, SmallInteger, TEXT, func, SmallInteger, or_
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from database import Base, connect_db


# 连接数据库
db = connect_db()


class User(Base):
    """ 用户 """
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    nickname: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    avatar: Mapped[str] = mapped_column(String(1024), nullable=True)
    sex: Mapped[int] = mapped_column(SmallInteger, server_default='0')  # 1 表示男, 2 表示女，0 表示未知
    company: Mapped[str] = mapped_column(String(255), nullable=True)
    intro: Mapped[str] = mapped_column(TEXT, nullable=True)
    role: Mapped[int] = mapped_column(SmallInteger, server_default='0')  # 0 表示普通用户, 100 表示管理员
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    
    # 小贴士, sqlalchemy 2.0 用法, 字段默认 NOT NULL, nullable=False 表示不可以为空
    
    
    def to_dict(self):
        
        # 性别处理
        sex = {
            1: '男',
            2: '女',
            0: '未知',
        }
        # 用户组处理
        role = {
            0: '普通用户',
            100: '管理员',
        }
        
        return {
            '编号': self.id,
            '用户名': self.username,
            '昵称': self.nickname,
            '邮箱': self.email,
            '头像': self.avatar,
            '性别': sex.get(self.sex),
            '公司.学校名': self.company,
            '简介': self.intro,
            '用户组': role.get(self.role),
            '创建时间': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            '更新时间': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
        }
        
        
    @staticmethod
    def add_user(username, nickname, password, email, sex):
        """ 添加用户 """
        
        condition_1 = or_(User.username == username, User.email == email)
        user = db.query(User).filter(condition_1).one_or_none()
        
        if not user:
            new_user = User(
                username=username, nickname=nickname, password=password, email=email, 
                avatar='default.jpeg', sex=sex, role=0, created_at=datetime.now(), updated_at=None,
            )

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            return new_user.to_dict()
        
        return None
        
    