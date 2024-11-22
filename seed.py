

# 种子, 填充数据库
from database import db, engine
from models.user import User
from models.post import Post
from models.user import Base as user_base
from models.post import Base as post_base


def create_table():
    
    """ 建表 """

    user_base.metadata.create_all(bind=engine)
    post_base.metadata.create_all(bind=engine)
    
    print('创建成功')

    

def batch_add_user():
    """ 批量插入用户数据 """
    users = [
        User(nickname='gua', password='123456', email='gua@vip.cn', avatar='doge.jpg'),
        User(nickname='jisoo', password='123456', email='jisoo@vip.cn', avatar='jisoo.jpg'),
    ]
    
    for e in users:
        db.add(e)
        db.commit()
    
    print('批量插入用户成功')


def batch_add_post():
    """ 批量插入帖子数据 """
    
    posts = [
        Post(
            title='个人转租, 整租两居室3000, 无中介', 
            content='地点, 铁心桥', 
            user_id=1, 
            is_draft=0,
        ),
        Post(
            title='标题 10', 
            content='炫狗', 
            user_id=1, 
            is_draft=0,
        ),
        Post(
            title='找个炮友, 18cm', 
            content='器大活好', 
            user_id=2, 
            is_draft=0,
        ),
        Post(
            title='标题 100', 
            content='梓神', 
            user_id=2, 
            is_draft=0,
        ),
    ]

    for e in posts:
        db.add(e)
        db.commit()

    print('批量插入帖子成功')
    
    
if __name__ == '__main__':    
    # 填充数据
    # create_table()  
    # batch_add_user()
    batch_add_post()
    
    
