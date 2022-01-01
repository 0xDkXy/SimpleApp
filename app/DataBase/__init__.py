import sqlite3
from loguru import logger
from hashlib import sha256
from ..tools.Logger import logger
import traceback

try:
    conn = sqlite3.connect('./data/user.db')
    logger.info('database conneted!')
    cur = conn.cursor()
    cur.execute('create table if not exists UserPasswd \
        (ID VARCHAR PRIMARY KEY     NOT NULL,\
        PASSWD VARCHAR NOT NULL\
        );\
    ')
    encry = sha256()
    encry.update(b'admin')
    hashAdminPwd = encry.hexdigest()
    Qstr = '\
    INSERT INTO UserPasswd (ID,PASSWD)\
    VALUES ("admin","{}")'.format(hashAdminPwd)
    cur.execute(Qstr)
    conn.commit()
except:
    logger.warning('database connect failed')
    logger.warning(traceback.format_exc())


# cur.execute('''
#     create table ''')
