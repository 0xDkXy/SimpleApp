from fastapi import APIRouter,Depends
from pydantic import BaseModel
from pydantic.errors import UrlSchemeError

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
    return {
        'id':user.id,
        'token':'xxxxxxx',
    }
