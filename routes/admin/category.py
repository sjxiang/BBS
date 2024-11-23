from flask import (
    Blueprint, request
)
from sqlalchemy import exc
import json

from models.category import Category

from utils.log import logger
from utils.serializer import (
    HttpCode, success, error
)


# 定义蓝图
main = Blueprint('category', __name__)


"""
新增课程分类
POST /admin/categories
"""
@main.route("/", methods=['POST'])
def create():

    data = json.loads(request.data)
    
    name = data['name']
    rank = data['rank']
    
    if not name:
        return error(code=HttpCode.params_error, msg='名称必须填写')
    
    if not rank:
        return error(code=HttpCode.params_error, msg='排序必须填写')
    
    if len(name) < 2 or len(name) > 45:
        return error(code=HttpCode.params_error, msg='名称长度必须在 2 ~ 45 之间')
    
    if int(rank) <= 0:
        return error(code=HttpCode.params_error, msg='排序值必须大于等于 0')
    
    
    try:
        new_category = Category.add_category(name=name, rank=int(rank))

        if not new_category:
            return error(code=HttpCode.record_already_exists, msg='名称已存在, 请选择其它名称')
        
        return success(msg="新增分类成功", data=new_category)
    
    except exc.SQLAlchemyError as e:
        logger.error('create_category error, {}'.format(e))
        return error(code=HttpCode.db_error, msg='数据库繁忙, 请稍后再试')


"""
课程分类列表
GET /admin/categories/all
"""
@main.route("/all", methods=['GET'])
def all():
    
    try:
        categories = Category.query_all()
        return success(msg="查询分类列表成功", data=categories)
    except exc.SQLAlchemyError as e:
        logger.error('query_all_category error, {}'.format(e))
        return error(code=HttpCode.db_error, msg='数据库繁忙, 请稍后再试')


"""
删除课程分类
DELETE /admin/categories/:id
"""
@main.route("/<int:id>", methods=['DELETE'])
def delete(id):
    pass


"""
课程分类详情
GET /admin/categories/:id
"""
@main.route("/<int:id>", methods=['GET'])
def show(id):
    pass


