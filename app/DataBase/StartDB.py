from sqlite3 import connect
from functools import wraps

def startDB(func):
    @wraps(func)
    def wrapper(*args,**kargs):
        db=connect('./data/user.db')
        cur=db.cursor()
        ret=func(*args,**kargs)
        queryVal=cur.execute(ret)
        db.commit()
        return queryVal.fetchall()
    return wrapper