from sqlite3 import connect

# loginDB=connect('user.db')

def insert(user:str,passwd:str):
    db=connect('user.db')
    cur=db.cursor()
    cur.execute('insert ')

def loginQuery(user:str,passwd:str)->bool:
    db=connect('./data/user.db')
    cur=db.cursor()
    Qstr='\
        SELECT PASSWD FROM UserPasswd\
        WHERE PASSWD = "{}"'.format(passwd)
    pwd=cur.execute(Qstr)
    db.commit()
    for row in pwd:
        if row[0]==passwd:
            return True
    return False
