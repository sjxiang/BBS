from flask import (
    Blueprint, request
)
from sqlalchemy import exc
import json

from models.setting import Setting

from utils.log import logger
from utils.serializer import (
    HttpCode, success, error
)


# 定义蓝图
main = Blueprint('setting', __name__)

"""
查询当前系统设置
GET /admin/settings
"""
@main.route("/", methods=['GET'])
def show():
    try:
        setting = Setting.find_one()
        
        if not setting:
            return error(code=HttpCode.record_not_found, msg='初始系统设置未找到, 请运行种子文件。')
        
        return success(msg="查询系统设置成功", data=setting)
    
    except exc.SQLAlchemyError as e:
        logger.error('query_setting error, {}'.format(e))
        return error(code=HttpCode.db_error, msg='数据库繁忙, 请稍后再试')



"""
更改系统设置
PUT /admin/settings
"""
@main.route("/", methods=['PUT'])
def update():

    data = json.loads(request.data)
    
    name = data['name']
    icp = data['icp']
    copyright = data['copyright']
    
    if not name or not icp or not copyright:
        return error(code=HttpCode.params_error, msg='请输入完整的系统设置信息。')
        
    try:
        resp = Setting.update(name, icp, copyright)
        
        if not resp:
            return error(code=HttpCode.record_not_found, msg='系统设置未找到, 请运行种子文件。')
        
        return success(msg="更改系统设置成功")
    
    except exc.SQLAlchemyError as e:
        logger.error('update_settings error, {}'.format(e))
        return error(code=HttpCode.db_error, msg='数据库繁忙, 请稍后再试')

