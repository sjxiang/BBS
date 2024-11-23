from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


""" 都是套路 """

# 数据库名称
database = 'bbs_api_development'

# 数据库连接配置
dsn = 'mysql+pymysql://root:my-secret-pw@127.0.0.1:13306/{}?charset=utf8mb4'.format(database)


# 1
engine = create_engine(dsn, echo=True)  

# 2
session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
# 线程安全
db = scoped_session(session)  

# 3, ORM 映射
Base = declarative_base()



def connect_db():
    """ 连接数据库 """
    return db


def connect_cache():
    """ 连接缓存 """
    pass