
from sqlalchemy import Integer, String, DateTime, TEXT, func, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from database import Base

        
class Setting(Base):
    __tablename__ = "settings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    icp: Mapped[str] = mapped_column(String(255), nullable=True)
    copyright: Mapped[str] = mapped_column(String(255), nullable=True)
    
    
    def to_dict(self):
        return {
            '编号': self.id,
            '项目名称': self.name,
            '备案号': self.icp,
            '版权信息': self.copyright,
        }