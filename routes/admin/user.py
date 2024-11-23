from flask import (
    Blueprint, request
)
from sqlalchemy import exc
import json, re

from models.user import User

from utils.log import logger
from utils.serializer import (
    HttpCode, success, error
)
from utils.common import check_password_strength, hashed_password

# 定义蓝图
main = Blueprint('user', __name__)

"""
查询用户详情
GET /admin/users/:id
"""
@main.route("/<int:id>", methods=['GET'])
def show():
    pass


"""
新增用户
POST /admin/users
"""
@main.route("/", methods=['POST'])
def create():
    data = json.loads(request.data)
    
    email = data.get('email')
    username = data.get('username')
    nickname = data.get('nickname')
    password = data.get('password')
    sex = data.get('sex')
    
    if not email:
        return error(code=HttpCode.params_error, msg='邮箱不能为空')
    if not username:
        return error(code=HttpCode.params_error, msg='用户名不能为空')
    if not nickname:
        return error(code=HttpCode.params_error, msg='昵称不能为空')
    if not password:
        return error(code=HttpCode.params_error, msg='密码不能为空')
    
    # fix bug, JSON 序列化 (integer, 0 等于 None)
    if sex is None:
        sex = 0
    if int(sex) not in [0, 1, 2]:
        return error(code=HttpCode.params_error, msg="性别的值只能是, 0 未选择, 1 男性, 2 女性")
    
    if not re.match(".+@.+\..+", email):
        return error(code=HttpCode.params_error, msg="邮箱格式不正确")
    
    # 校验密码强度
    if not check_password_strength(password):
        return error(code=HttpCode.params_error, msg="密码必须包含大小写字母和数字的组合, 不能使用特殊字符, 长度在8-30之间")

    try:
        new_user = User.add_user(email=email, username=username, nickname=nickname, password=hashed_password(password), sex=int(sex))
    
        if not new_user:
            return error(code=HttpCode.record_already_exists, msg='邮箱\用户名已存在, 请直接登录')
        
        return success(msg='新增用户成功', data=new_user)
    
    except exc.SQLAlchemyError as e:
        logger.error('create_user error, {}'.format(e))
        return error(code=HttpCode.db_error, msg='数据库繁忙, 请稍后再试')
    