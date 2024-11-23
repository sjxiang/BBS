from flask import (
    Blueprint, request
)
from sqlalchemy import exc
import json

from models.post import Post 

from utils.log import logger
from utils.serializer import (
    HttpCode, success, error
)


# 定义蓝图
main = Blueprint('post', __name__)


"""
查询帖子列表, 分页查询
GET /admin/posts/all?pageNum=1&pageSize=10
"""
@main.route("/all", methods=['GET'])
def paging():
    # 当前是第几页, 如果不传则默认为第一页
    page_num = request.args.get("pageNum", default=1, type=int)
    # 每页显示多少条数据, 如果不传则默认为10条
    page_size = request.args.get("pageSize", default=10, type=int)
    
    try:        
        total_count, total_pages, items = Post.query_all_by_page(page_size, page_num)
        
        return success(msg="查询文章列表成功", data={"posts": items, "pagination": {"total_count": total_count, "total_pages": total_pages}})
 
    except exc.SQLAlchemyError as e:
        logger.error('query_post_ error, {}'.format(e))
        return error(HttpCode.db_error, msg="查询文章列表失败")
    
            

"""
查询帖子详情
GET /admin/posts/<id>
"""
@main.route("/<int:id>", methods=['GET'])
def show(id):

    if id <= 0:
        return error(HttpCode.params_error, msg="请求参数错误")
    
    try:
        post = Post.query_post_by_id(id)
        
        if not post:
            return error(HttpCode.record_not_found, msg="文章未找到")
        
        return success(msg="查询文章详情成功", data=post)
    
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
        return error(HttpCode.params_error, msg="请求参数不能为空")
    
    if int(user_id) <= 0:
        return error(HttpCode.params_error, msg="请求参数非法")
    
    try:
        new_post = Post.add_post(title, content, int(user_id))
        return success(msg="创建文章成功", data=new_post)
    
    except exc.SQLAlchemyError as e:
        logger.error('create_post error, {}'.format(e))    
        return error(HttpCode.db_error, msg="创建文章失败")
    
    

"""
删除文章
DELETE /admin/posts/<id>
"""
@main.route("/<int:id>", methods=['DELETE'])
def destroy(id):
    
    if int(id) <= 0:
        return error(HttpCode.params_error, msg="请求参数id无效")

    try:
        resp = Post.delete_post(id)
       
        if not resp:
           return error(HttpCode.record_not_found, msg="文章未找到")
       
        return success(msg="删除文章成功")
    
    except exc.SQLAlchemyError as e:
        logger.error('delete_post error, {}'.format(e))
        return error(HttpCode.db_error, msg="删除文章失败")


"""
更新文章
PUT /admin/posts/<id>
"""
@main.route("/<int:id>", methods=['PUT'])
def update(id):
    data = json.loads(request.data)
        
    title = data['title']
    content = data['content']
    
    if id <= 0:
        return error(HttpCode.params_error, msg="请求参数id无效")
    
    if not title:
        return error(HttpCode.params_error, msg="标题不能为空")

    try:        
        resp = Post.mod_post(id, title, content)
        
        if not resp:
            return error(HttpCode.record_not_found, msg="文章未找到")
                   
        return success(msg="更新文章成功")

    except exc.SQLAlchemyError as e:
        logger.error('update_post error, {}'.format(e))
        return error(HttpCode.db_error, msg="更新文章失败")



"""
发布文章
PUT /admin/posts/<id>/publish
"""
@main.route("/<int:id>/publish", methods=['PUT'])
def publish(id):
    
    if id <= 0:
        return error(HttpCode.params_error, msg="请求参数id无效")

    try:
        
        resp = Post.mod_draft(id)
        
        if not resp:
            return error(HttpCode.record_not_found, msg="文章未找到")
        
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

    query = request.args.get("query", default=None, type=str)
    
    if not query:
        return error(HttpCode.params_error, msg="参数不能为空")
    
    try:
        resp = Post.query_post_by_field(query)
        
        if len(resp) == 0:
            return success(msg="数据为空")
        
        return success(msg="搜索文章成功", data=resp)
    except exc.SQLAlchemyError as e:
        logger.error('search_post error, {}'.format(e))
        return error(HttpCode.db_error, msg="搜索文章失败")
