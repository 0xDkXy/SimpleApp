from .StartDB import startDB

@startDB
def query(user:str):
    Qstr='SELECT CID,CNAME,ADDRES,PHONE\
        FROM customer\
        WHERE UID="{}"'.format(user)
    return Qstr


@startDB
def insert(cIf):
    '''
    cIf :customere infomation
    '''
    try:
        Qstr='INSERT INTO customer (CID,CNAME,ADDRES,PHONE,UID)\
        VALUES ("{}","{}","{}","{}","{}")'.format(
            cIf['CID'],
            cIf['CName'],
            cIf['addres'],
            cIf['phone'],
            cIf['UID']) 
        return Qstr
    except Exception as e:
        raise e



