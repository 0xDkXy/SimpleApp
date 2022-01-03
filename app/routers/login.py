from typing import Optional
from fastapi import APIRouter,Depends
from pydantic import BaseModel
from hashlib import sha256
from ..DataBase.loginDB import SignIn, SignUp
from ..core.aliveList import aliveUpdate
from ..tools.token import getToken

class User(BaseModel):
    id:str
    passwd:Optional[str]

router=APIRouter(
    prefix='/login',
    tags=['login'],
    responses={404:{"description":'Not found'}},
)


# sha256 hash 函数
def encry(input:str)->str:
    input=input.encode()
    sha_256=sha256()
    sha_256.update(input)
    ret=sha_256.hexdigest()
    del sha_256
    return ret


@router.post('/signIn')
def signIn(user:User):
    pwdSha256=encry(user.passwd)
    token=getToken()# 获取token
    aliveUpdate({user.id:token}) 
    if SignIn(user=user.id,passwd=pwdSha256):return {
            'id':user.id,
            'token':token,
            'msg':'signIn successfully'
        }
    else:
        return {'msg':'Wrong ID or Passwords',}

@router.post('/signUp')    
def signUp(user:User):
    pwdSha256=encry(user.passwd)
    if SignUp(user.id,pwdSha256):
        return{
            'msg':'signUp successfully',
        }
    else:
        return {'msg':'repeated ID'}
    
