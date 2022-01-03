from typing import Optional
from fastapi import APIRouter
from qrcode import image
from qrcode.image import base
from ..tools.Logger import logger 
from pydantic import BaseModel
from app.tools import token
from .login import User
from app import routers
from ..DataBase.customerDB import query,insert
from ..core.aliveList import *
from ..core.aliveList import aliveVerify
from traceback import format_exc
import qrcode
from fastapi.responses import FileResponse
import base64


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

@router.post('/getCostInfoAll')
def getCostInfoAll(input:userVerify):
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
        ret=str(ret).encode()
        ret=base64.b64encode(ret).decode()
        logger.info("UID:{} | ret:{}".format(UID,ret))
        img=qrcode.make(ret)
        imgPath='./data/{}_qrcode.png'.format(UID)
        with open(imgPath,'wb') as f:
            img.save(f)
        return FileResponse(path=imgPath,filename=imgPath.split('/')[2])
        # return 
    else:
        return {'msg':'wrong token'}
            

