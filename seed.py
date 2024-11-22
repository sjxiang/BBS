

# 种子, 填充数据库
from database import db, engine
from models.user import User
from models.post import Post
from models.category import Category
from models.course import Course

from models.user import Base as user_base
from models.post import Base as post_base
from models.category import Base as category_base
from models.course import Base as course_base
from models.chapter import Base as chapter_base
from models.like import Base as like_base
from models.setting import Base as setting_base


def create_table():
    
    """ 建表 """
    
    # 用户表
    user_base.metadata.create_all(bind=engine)
    # 帖子表
    post_base.metadata.create_all(bind=engine)
    # 分类表
    category_base.metadata.create_all(bind=engine)
    # 课程表
    course_base.metadata.create_all(bind=engine)
    # 章节表
    chapter_base.metadata.create_all(bind=engine)
    # 点赞表
    like_base.metadata.create_all(bind=engine)
    # 系统设置表
    setting_base.metadata.create_all(bind=engine)
    
    print('创建成功')

    

def batch_add_user():
    """ 批量插入用户数据 """
    users = [
        User(username='gua', nickname='gua', password='123456', email='gua@vip.cn', avatar='doge.jpg'),
        User(username='jisoo', nickname='jisoo', password='123456', email='jisoo@vip.cn', avatar='jisoo.jpg'),
    ]
    
    for e in users:
        db.add(e)
        db.commit()
    
    print('批量插入用户成功')


def batch_add_post():
    """ 批量插入帖子数据 """
    
    posts = [
        Post(title='个人转租, 整租两居室3000, 无中介', content='地点, 铁心桥', user_id=1, is_draft=0),
        Post(title='标题 10', content='炫狗', user_id=1, is_draft=0),
        Post(title='找个炮友, 18cm', content='器大活好', user_id=2, is_draft=0),
        Post(title='标题 100', content='梓神', user_id=2, is_draft=0),
    ]

    for e in posts:
        db.add(e)
        db.commit()

    print('批量插入帖子成功')


def batch_add_category():
    """ 批量插入分类数据 """

    categories = [
        Category(name='前端', rank=10),
        Category(name='后端', rank=100),
        Category(name='测试', rank=2),
    ]
    for e in categories:
        db.add(e)
        db.commit()
    print('批量插入分类成功')
    
    
def batch_add_course():
    """ 批量插入课程数据 """

    courses = [
        Course(category_id="2", name='golang 初级训练营', user_id=1),
        Course(category_id="1", name='vue3 实战', user_id=1),
        Course(category_id="2", name='golang 架构训练营', user_id=1),
    ]
    for e in courses:
        db.add(e)
        db.commit()
    print('批量插入课程成功')
    
    
if __name__ == '__main__':    
    # 填充数据
    create_table()  
    # batch_add_user()
    # batch_add_post()
    # batch_add_category()
    
    # pass
    # batch_add_course()
    
