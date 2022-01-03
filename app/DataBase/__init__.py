import sqlite3
from loguru import logger
from hashlib import sha256
from ..tools.Logger import logger
import traceback,os

# 创建数据存放目录
if not os.path.exists(r'./data'):
    os.mkdir(r'data')

try:
    conn = sqlite3.connect('./data/user.db')
    logger.info('database conneted!')
    cur = conn.cursor()
    cur.execute('create table if not exists UserPasswd \
        (ID VARCHAR PRIMARY KEY     NOT NULL,\
        PASSWD VARCHAR NOT NULL\
        );\
    ')
    conn.commit()
    encry = sha256()
    encry.update(b'admin')
    hashAdminPwd = encry.hexdigest()
    Qstr='select ID,PASSWD FROM UserPasswd\
        WHERE ID="{}" and PASSWD="{}"'.format('admin',hashAdminPwd)
    val=cur.execute(Qstr)
    conn.commit()
    if not val:
        Qstr = '\
        INSERT INTO UserPasswd (ID,PASSWD)\
        VALUES ("admin","{}")'.format(hashAdminPwd)
        cur.execute(Qstr)
        conn.commit()
        logger.info('创建管理员账户成功！')
    else:
        logger.info('已有管理员账户')
    cur.execute('create table if not exists customer \
        (CID VARCHAR NOT NULL,\
        CNAME VARCHAR NOT NULL,\
        ADDRES TEXT NOT NULL,\
        PHONE VARCHAR,\
        UID VARCHAR NOT NULL\
        );\
    ')
except:
    logger.warning('database connect failed')
    logger.warning(traceback.format_exc())
finally:
    conn.close()


# cur.execute('''
#     create table ''')
