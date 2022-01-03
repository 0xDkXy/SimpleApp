from .StartDB import startDB


@startDB
def signIn(user:str,passwd:str):
    Qstr='\
        SELECT PASSWD FROM UserPasswd\
        WHERE ID = "{}"'.format(user)
    return Qstr

def SignIn(user:str,passwd:str)->bool:
    val=signIn(user,passwd)
    # print(list(val))
    return True if val[0][0]==passwd else False

@startDB
def signUp(user:str,passwd:str):
    Qstr = '\
        INSERT INTO UserPasswd (ID,PASSWD)\
        VALUES ("{}","{}")'.format(user,passwd)
    return Qstr

def SignUp(user:str,passwd:str)->bool:
    val=signIn(user,passwd)
    if val:
        return False
    else:
        signUp(user,passwd)
        return True