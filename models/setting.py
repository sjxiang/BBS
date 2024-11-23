from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from database import Base, connect_db


# 连接数据库
db = connect_db()

        
class Setting(Base):
    """ 系统设置 """
    
    __tablename__ = "settings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    icp: Mapped[str] = mapped_column(String(255), nullable=True)
    copyright: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    
    def to_dict(self):
        return {
            '编号': self.id,
            '项目名称': self.name,
            '备案号': self.icp,
            '版权信息': self.copyright,
            '创建时间': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            '更新时间': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
        }
        
    
    @staticmethod
    def find_one() -> dict | None:
        
        setting = db.query(Setting).filter(Setting.id == 1).one_or_none()
        
        if not setting:
            return None
        
        return setting.to_dict()
    
    
    @staticmethod
    def update(name, icp, copyright) -> str | None:
        
        setting = db.query(Setting).filter(Setting.id == 1).one_or_none()
        
        if not setting:
            return None
        
        setting.name = name
        setting.icp = icp
        setting.copyright = copyright
        setting.updated_at = datetime.now()
        
        db.commit()
        
        return '修改成功'
    