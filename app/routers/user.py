from typing import Optional
from fastapi import APIRouter
from ..tools.Logger import logger 
from pydantic import BaseModel
from app.tools import token
from .login import User
from app import routers
from ..DataBase.customerDB import query,insert
from ..core.aliveList import *
from ..core.aliveList import aliveVerify
from traceback import format_exc


class customer(BaseModel):
    CID:str
    CName:str
    addres:str
    phone:str
    UID:Optional[str]
    token:Optional[str]

class userVerify(BaseModel):
    UID:str
    token:str

router=APIRouter(
    prefix='/user',
    tags=['customer'],
    responses={404:{'description':'Not found'}},
)


@router.post('/addInfo')
def addCustomer(input:customer):
    token=input.token
    UID=input.UID
    if token == None or UID == None :
        return {'msg':'permission denied'}
    if aliveVerify('admin',token):
        try:
            insert(input.dict())
            return {'msg':'customer info update successed!'}
        except:
            logger.error(format_exc())
            return {'msg':'wrong info'}
    else:
        return {'msg':'wrong token'}
    
@router.post('/getCostInfo')
def getCostInfo(input:userVerify):
    token=input.token
    UID=input.UID
    if token == None or UID == None :
        return {'msg':'permission denied'}
    if aliveVerify(UID,token):
        try:
            List=query(UID)
        except Exception as e:
            raise e
        ret={}
        for p,info in enumerate(List):
            ret.update({
                str(p):{
                    'CID':info[0],
                    'CName':info[1],
                    'addres':info[2],
                    'phone':info[3],
                }
            })
        return ret
    else:
        return {'msg':'wrong token'}

            

