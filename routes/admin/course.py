from flask import (
    Blueprint, request
)
from sqlalchemy import exc
import json, re

from models.course import Course

from utils.log import logger
from utils.serializer import (
    HttpCode, success, error
)

# 定义蓝图
main = Blueprint('course', __name__)

"""
查询课程详情
GET /admin/courses/:id
"""
@main.route("/<int:id>", methods=['GET'])
def show(id):
    pass


"""
查询课程列表
GET /admin/courses/all
"""
@main.route("/all", methods=['GET'])
def all():
    try:
        resp = Course.query_all()
        return success(msg="查询课程详情成功", data=resp)
    
    except exc.SQLAlchemyError as e:
        logger.error('query_course error, {}'.format(e))
        return error(HttpCode.db_error, msg="查询课程详情失败")


"""
添加课程
POST /admin/courses
"""
@main.route("/", methods=['POST'])
def create():
    data = json.loads(request.data)
    
    category_id = data.get('category_id')
    user_id = data.get('user_id')
    
    if not category_id:
        return error(HttpCode.BAD_REQUEST, '分类编号不能为空')
    
    if not user_id:
        return error(HttpCode.BAD_REQUEST, '用户编号不能为空')
    
    
    # 的分类不存在
    # 的用户不存在

