from flask import Flask

app = Flask(__name__)

# 注册蓝图

# 后台接口
from routes.admin.post import main as admin_post_routes
from routes.admin.category import main as admin_category_routes
from routes.admin.setting import main as admin_setting_routes
from routes.admin.user import main as admin_user_routes
from routes.admin.course import main as admin_course_routes

app.register_blueprint(admin_post_routes, url_prefix='/admin/posts')
app.register_blueprint(admin_category_routes, url_prefix='/admin/categories')
app.register_blueprint(admin_setting_routes, url_prefix='/admin/settings')
app.register_blueprint(admin_user_routes, url_prefix='/admin/users')
app.register_blueprint(admin_course_routes, url_prefix='/admin/courses')


# 运行代码
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=9000,
    )    
    app.run(**config)


