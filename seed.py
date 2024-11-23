

# 种子, 填充数据库

from database import db, engine
from models.user import User
from models.post import Post
from models.category import Category
from models.course import Course
from models.chapter import Chapter
from models.like import Like
from models.setting import Setting

from models.user import Base as user_base
from models.post import Base as post_base
from models.category import Base as category_base
from models.course import Base as course_base
from models.chapter import Base as chapter_base
from models.like import Base as like_base
from models.setting import Base as setting_base

from utils.common import hashed_password
from datetime import datetime

def log(*args, **kwargs):
    """
    打印日志
    """
    # 获取当前日期和时间
    now = datetime.now()
    # 将其格式化为字符串, 例如 "2024/10/29 17:25:23"
    formatted_date = now.strftime('%Y/%m/%d %H:%M:%S')

    # 输出1
    print('<log>', formatted_date, *args, **kwargs)

    # 输出2
    with open('gua.log', 'a', encoding='utf-8') as f:
        print(formatted_date, *args, file=f, **kwargs)
    
        

def create_table():
    
    """ 建表 """
    
    user_base.metadata.create_all(bind=engine)
    log('bbs, 数据表 {} 建表成功！'.format('用户表'))
    
    post_base.metadata.create_all(bind=engine)
    log('bbs, 数据表 {} 建表成功！'.format('帖子表'))
    
    category_base.metadata.create_all(bind=engine)
    log('bbs, 数据表 {} 建表成功！'.format('分类表'))
    
    course_base.metadata.create_all(bind=engine)
    log('bbs, 数据表 {} 建表成功！'.format('课程表'))
    
    chapter_base.metadata.create_all(bind=engine)
    log('bbs, 数据表 {} 建表成功！'.format('章节表'))
    
    like_base.metadata.create_all(bind=engine)
    log('bbs, 数据表 {} 建表成功！'.format('点赞表'))
    
    setting_base.metadata.create_all(bind=engine)
    log('bbs, 数据表 {} 建表成功！'.format('系统设置表'))
    
    log('bbs, 数据库初始化完成！')
    
    

def batch_add_user():
    """ 批量插入用户数据 """
    users = [
        User(username='gua1997', nickname='瓜', password=hashed_password('123456'), email='gua@vip.cn', avatar='doge.jpg'),
        User(username='jisoo98', nickname='金智秀', password=hashed_password('123456'), email='jisoo@vip.cn', avatar='jisoo.jpg'),
    ]
    
    for e in users:
        db.add(e)
        db.commit()
    
    log('批量插入用户, 成功')


def batch_add_post():
    """ 批量插入帖子数据 """
    
    posts = [
        Post(title='个人转租, 整租两居室3000, 无中介', content='临近地铁口', user_id=1, is_draft=0),
        Post(title='找个炮友, 坐标浦口', content='器大活好', user_id=2, is_draft=0),
        Post(title='标题 10', content='炫狗', user_id=1, is_draft=0),
        Post(title='标题 100', content='梓神', user_id=2, is_draft=0),
        Post(title='标题 1000', content='甜甜甜', user_id=2, is_draft=0),
    ]

    for e in posts:
        db.add(e)
        db.commit()

    log('批量插入帖子, 成功')


def batch_add_category():
    """ 批量插入分类领域数据 """

    categories = [
        Category(id=1, name='后端/架构', rank=1),
        Category(id=2, name='前端/移动', rank=2),
        Category(id=3, name='计算机基础', rank=3),
        Category(id=4, name='AI/大数据', rank=4),
        Category(id=5, name='运维/测试', rank=5),
        Category(id=6, name='产品/运营', rank=6),
        Category(id=7, name='管理/成长', rank=7),
    ]
    
    for e in categories:
        db.add(e)
        db.commit()
    
    log('批量插入课程分类, 成功')
    
    
def batch_add_course():
    """ 批量插入课程数据 """

    courses = [
        Course(category_id="2", name='Electron+Vue3+AI+云存储, 实战跨平台桌面应用', user_id=1),
        Course(category_id="2", name='前端全栈进阶, Nextjs 打造框架 SaaS 应用', user_id=1),
        Course(category_id="1", name='AI助手Copilot辅助Go+Flutter, 打造全栈式在线教育系统', user_id=1),
        Course(category_id="1", name='Python Flask 高级编程, 从0到1开发《鱼书》精品项目', user_id=1),
        Course(category_id="1", name='Python 量化交易系统实战', user_id=1),
    ]
    for e in courses:
        db.add(e)
        db.commit()
        
    log('批量插入课程, 成功')


def batch_add_settings():
    """ 批量插入系统设置数据 """
    
    setting = Setting(
        name='bbs论坛', 
        icp='苏ICP备123456789号', 
        copyright='© 2023 bbs论坛 版权所有', 
        created_at=datetime.now(),
    )
    db.add(setting)
    db.commit()
        
    log('插入系统设置, 成功')
    
    
    
def seed():
    """ 填充数据 """
    batch_add_user()
    batch_add_post()
    batch_add_category()
    batch_add_course()
    batch_add_settings() 
    

if __name__ == '__main__':    

    # create_table()  
    seed()

    
