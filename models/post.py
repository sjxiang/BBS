from sqlalchemy import Integer, String, DateTime, TEXT, func, SmallInteger, or_
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from database import Base, connect_db
from models.user import User
        

# 连接 db
db = connect_db()

        
class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))                          
    content: Mapped[str] = mapped_column(TEXT)                               
    user_id: Mapped[int] = mapped_column(Integer)                            
    is_draft: Mapped[int] = mapped_column(SmallInteger, server_default='1')  
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    
    def to_dict(self):
        
        state = {
            0: '已发布',
            1: '还在起草中',
        }
        
        return {
            '编号': self.id,
            '标题': self.title,
            '内容': self.content,
            '作者': self.user_id,
            '进展': state.get(self.is_draft),
            '创建时间': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            '更新时间': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None,
        }
        
    
    @staticmethod
    def query_all_by_page(page_size, page_num):
        """ 分页查询 """
        
        total_count = db.query(Post).filter(Post.is_draft == 0).count()
        total_pages = (total_count + page_size - 1) // page_size    
        # 计算跳过的记录数
        skip = (page_num - 1) * page_size
        
        result = db.query(Post).filter(Post.is_draft == 0).order_by(Post.id.desc()).limit(page_size).offset(skip).all()
        
        items = []
    
        for e in result:
            items.append(e.to_dict())

        return total_count, total_pages, items
      
      
    @staticmethod
    def query_post_by_id(post_id):
        """ 根据帖子编号查询 """

        post = db.query(Post).filter(Post.id == post_id).one_or_none()
        
        if not post:
            return None
    
        return post.to_dict()
        
        
    @staticmethod
    def delete_post(post_id):
        """ 硬删除 """
        # 查询当前文章        
        post = db.query(Post).filter(Post.id == post_id)

        # 判断当前文章是否存在
        if not post.first():
            return None

        post.delete(synchronize_session=False)  # 另一种方案, 软删除(status, 默认0, 1 表示已删除)
        
        db.commit()
        
        return "删除成功"


    @staticmethod
    def mod_post(post_id, title, content):
        """ 更新 """
        
        post = db.query(Post).filter(Post.id == post_id).one_or_none()
        
        if not post:
            return None
            
        post.title = title
        post.content = content
        post.updated_at = datetime.now()
        
        db.commit()
        
        return '修改成功'
    
    
    @staticmethod
    def mod_draft(post_id):
        """ 修改草稿 """

        post = db.query(Post).filter(Post.id == post_id).one_or_none()

        if not post:
            return None

        post.is_draft = 0
        post.updated_at = datetime.now()

        db.commit()
        
        return '更新成功'        
    
    
    @staticmethod
    def add_post(title, content, user_id):
        """ 添加 """
        
        new_post = Post(title=title, content=content, user_id=user_id, is_draft=1, created_at=datetime.now(), updated_at=None)
        
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        
        return new_post.to_dict()
    
    
    @staticmethod
    def query_post_by_field(keyword):
        """ 根据关键词查询 """
       
        condition_1 = or_(Post.title.like(f'%{keyword}%'), Post.content.like(f'%{keyword}%'))
        
        result = db.query(Post, User.nickname).join(User.id == Post.user_id).filter(condition_1, Post.is_draft == 0).all()
        
        resp = build_resp(result)
        return resp
    


    
    
def build_resp(rows):
    """
    (variable) List[Post]
    (variable) List[Row[Tuple[Post, str]]]
    
    """
    converted_result = []
    
    for row in rows:
        post, nickname = row  # 获取元组中的 Post 对象和字符串
        
        item = {}
        item["用户昵称"] = nickname
        item["标题"] = post.title
        item["正文内容"] = post.content
        item["创建时间"] = post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        item["更新时间"] = post.updated_at.strftime('%Y-%m-%d %H:%M:%S') if post.updated_at else None
        
        converted_result.append(item)

    return converted_result



