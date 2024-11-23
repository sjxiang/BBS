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
    pass


"""
删除课程分类
DELETE /admin/categories
"""
@main.route("/", methods=['DELETE'])
def delete():
    pass


"""
课程分类列表
GET /admin/categories/all
"""
@main.route("/all", methods=['GET'])
def all():
    pass



"""
课程分类详情
GET /admin/categories/:id
"""
@main.route("/<int:id>", methods=['GET'])
def show():
    pass


