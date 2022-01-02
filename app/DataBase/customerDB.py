from StartDB import startDB

@startDB
def query(user:str):
    Qstr='SELECT CID,CNAME,ADDRES,PHONE\
        FROM customer\
        WHERE UID="{}"'.format(user)
    return Qstr


@startDB
def insert(CID:str,CNAME:str,UID:str,ADDRES:str,PHONE:str):
    Qstr='INSERT INTO customer (CID,CNAME,UID,ADDRES,PHONE)\
        VALUES ("{}","{}","{}","{}","{}")'.format(CID,CNAME,UID,ADDRES,PHONE) 
    return Qstr



