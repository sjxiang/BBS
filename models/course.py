from sqlalchemy import Integer, String, DateTime, TEXT, func, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column
from database import Base, connect_db

from datetime import datetime
from models.user import User
from models.category import Category


# 连接数据库
db = connect_db()



class Course(Base):
    """ 课程 """
    
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
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    
    
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
            '创建时间': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            '更新时间': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
        }
            

    def add_course(category_id, name, user_id, image, recommended, introductory, content) -> dict | None:
        """ 添加课程 """

        new_course = Course(
            category_id=category_id,
            name=name,
            user_id=user_id,
            image=image,
            recommended=recommended,
            introductory=introductory,
            content=content,
            likes_count=0,
            chapters_count=0,
            created_at=datetime.now(),
            updated_at=None,
        )

        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        
        return new_course.to_dict()
    
    
    @staticmethod
    def query_all() -> list:
        """ 查询所有 """

        result = db.query(Course, Category.name, User.username).join(User, User.id == Course.user_id).join(Category, Category.id == Course.category_id).order_by(Course.id.desc()).all()
        return build_resp(result)


def build_resp(rows):
    """
    (variable) List[Row[Tuple[Course, str, str]]]
    (variable) List[Post]
    
    """
    converted_result = []
    
    for row in rows:
        course, category_name, username = row  # 获取元组中的 Course 对象和字符串
        
        item = {}
        item["课程名称"] = course.name
        item['课程分类'] = category_name
        item['课程讲师'] = username
        item['课程图片'] = course.image
        item['课程内容'] = course.content
        item['是否推荐'] = course.recommended == 1
        item['是否为入门课程'] = course.introductory == 1
        item['课程的点赞数'] = course.likes_count
        item['课程的章节数量'] = course.chapters_count,
        item['创建时间'] = course.created_at.strftime('%Y-%m-%d %H:%M:%S')
        item['更新时间'] = course.updated_at.strftime('%Y-%m-%d %H:%M:%S') if course.updated_at else None
        
        converted_result.append(item)

    return converted_result


