from fastapi import APIRouter,Depends
from pydantic import BaseModel
from pydantic.errors import UrlSchemeError
from hashlib import sha256
from ..DataBase.loginDB import loginQuery 

class loginModel(BaseModel):
    id:str
    passwd:str

router=APIRouter(
    prefix='/login',
    tags=['login'],
    responses={404:{"description":'Not found'}},
)

@router.post('/')
async def loginRoot(user:loginModel):
    encry=sha256()
    pwd=user.passwd.encode()
    encry.update(pwd)
    pwdSha256=encry.hexdigest()
    del encry
    if loginQuery(user=user.id,passwd=pwdSha256):return {
            'id':user.id,
            'token':'',
            'sha256':pwdSha256,
        }
    else:
        return {'msg':'wa',}

    
