from flask import (
    Blueprint, request
)
from sqlalchemy import exc, or_
from datetime import datetime
import json

from models.post import Post as model_post
from models.user import User as model_user

from utils.log import logger
from utils.serializer import (
    HttpCode, success, error
)
from database import connect_db


# 定义蓝图
main = Blueprint('post', __name__)

# 连接数据库
db = connect_db()


"""
查询帖子列表, 分页查询
GET /admin/posts/all?currentPage=2&pageSize=10
"""
@main.route("/all", methods=['GET'])
def paging():
    
    # 当前是第几页, 如果不传则默认为第一页
    current_page = request.args.get("currentPage")
    # 每页显示多少条数据, 如果不传则默认为10条
    page_size = request.args.get("pageSize")
    
    if not current_page or not page_size:
        current_page, page_size = 1, 10
    
    page_size = int(page_size)
    current_page = int(current_page)
    
    try:        
        total_count = db.query(model_post).count()
        total_pages = (total_count + page_size - 1) // page_size

        skip = (current_page - 1) * page_size           
            
        result = db.query(model_post).filter(model_post.is_draft == 0).order_by(model_post.id.desc()).limit(page_size).offset(skip).all()
        
        resp = []
        for e in result:
            resp.append(e.to_dict())

        return success(msg="查询文章列表成功", data={"posts": resp, "pagination": {"total_count": total_count, "total_pages": total_pages}})
 
    except exc.SQLAlchemyError as e:
        logger.error('query_post_ error, {}'.format(e))
        return error(HttpCode.db_error, msg="查询文章列表失败")
    
            

"""
查询帖子详情
GET /admin/posts/<id>
"""
@main.route("/<id>", methods=['GET'])
def show(id):

    if int(id) <= 0:
        return error(HttpCode.params_error, msg="请求参数错误")
    
    try:
        post = db.query(model_post).filter(model_post.id == id).one_or_none()
        
        if not post:
            return error(HttpCode.record_not_found, msg="文章未找到")
        
        return success(msg="查询文章详情成功", data=post.to_dict())
    
    except exc.SQLAlchemyError as e:
        logger.error('query_post_detail_by_id error, {}'.format(e))
        return error(HttpCode.db_error, msg="查询文章详情失败")
    
    
    
"""
创建文章
POST /admin/posts
"""
@main.route("/", methods=['POST'])
def create():
    data = json.loads(request.data)
    
    title = data['title']
    content = data['content']
    user_id = data['user_id']
    
    # 验证参数
    if not title or not user_id:
        return error(HttpCode.params_error, msg="参数不能为空")
    
    if int(user_id) <= 0:
        return error(HttpCode.params_error, msg="请求参数非法")
    
    try:
        new_post = model_post(title=title, content=content, user_id=int(user_id), is_draft=1, created_at=datetime.now(), updated_at=None)
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return success(msg="创建文章成功", data=new_post.to_dict())
    
    except exc.SQLAlchemyError as e:
        logger.error('create_post error, {}'.format(e))    
        return error(HttpCode.db_error, msg="创建文章失败")
    
    

"""
删除文章
DELETE /admin/posts/<id>
"""
@main.route("/<id>", methods=['DELETE'])
def destroy(id):
    
    if int(id) <= 0:
        return error(HttpCode.params_error, msg="请求参数错误")

    try:
        # 查询当前文章
        post = db.query(model_post).filter(model_post.id == int(id))
        
        # 判断当前文章是否存在
        if not post.first():
            return error(HttpCode.record_not_found, msg="文章未找到")
        
        post.delete(synchronize_session=False)
        
        db.commit()
        return success(msg="删除文章成功")
    
    except exc.SQLAlchemyError as e:
        logger.error('delete_post error, {}'.format(e))
        return error(HttpCode.db_error, msg="删除文章失败")


"""
更新文章
PUT /admin/posts/<id>
"""
@main.route("/<id>", methods=['PUT'])
def update(id):
    data = json.loads(request.data)
        
    title = data['title']
    content = data['content']
    
    if int(id) <= 0:
        return error(HttpCode.params_error, msg="请求参数错误")
    
    if not title:
        return error(HttpCode.params_error, msg="标题不能为空")

    try:        
        post = db.query(model_post).filter(model_post.id == int(id)).one_or_none()
        
        if not post:
            return error(HttpCode.record_not_found, msg="文章未找到")
            
        post.title = title
        post.content = content
        post.updated_at = datetime.now()
        
        db.commit()        
        return success(msg="更新文章成功")

    except exc.SQLAlchemyError as e:
        logger.error('update_post error, {}'.format(e))
        return error(HttpCode.db_error, msg="更新文章失败")



"""
发布文章
PUT /admin/posts/<id>/publish
"""
@main.route("/<id>/publish", methods=['PUT'])
def publish(id):
    if int(id) <= 0:
        return error(HttpCode.params_error, msg="参数错误")

    try:
        post = db.query(model_post).filter(model_post.id == int(id)).one_or_none()

        if not post:
            return error(HttpCode.record_not_found, msg="文章未找到")

        post.is_draft = 0
        post.updated_at = datetime.now()

        db.commit()
        return success(msg="发布文章成功")
    
    except exc.SQLAlchemyError as e:
        logger.error('publish_post error, {}'.format(e))
        return error(HttpCode.db_error, msg="发布文章失败")
    


"""
搜索文章
PUT /admin/posts/search?query=转租
"""
@main.route("/search", methods=['GET'])
def search():
    query = request.args.get("query")
    
    if not query:
        return error(HttpCode.params_error, msg="参数错误")
    
    try:
        condition_1 = or_(
            model_post.title.like('%{}%'.format(query)), 
            model_post.content.like('%{}%'.format(query)),
        )
        rows = db.query(model_post, model_user.nickname).join(model_user, model_user.id == model_post.user_id).filter(condition_1, model_post.is_draft == 0).all() 
        resp = build_resp(rows)
            
        return success(msg="搜索文章成功", data=resp)
    except exc.SQLAlchemyError as e:
        logger.error('search_post error, {}'.format(e))
        return error(HttpCode.db_error, msg="搜索文章失败")




def build_resp(rows):
    """
    (variable) List[Post]
    (variable) List[Row[Tuple[Post, str]]]
    
    """
    
    converted_result = []
    
    for row in rows:
        post, nickname = row  # 获取元组中的 Post 对象和字符串
        
        item = {}
        item["用户"] = nickname
        item["标题"] = post.title
        item["正文内容"] = post.content
        item["创建时间"] = post.created_at.strftime('%Y-%m-%d %H:%M:%S')
        item["更新时间"] = post.updated_at.strftime('%Y-%m-%d %H:%M:%S') if post.updated_at else None
        
        converted_result.append(item)

    return converted_result

