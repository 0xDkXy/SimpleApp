from typing import Optional
from fastapi import APIRouter,status
from qrcode import image
from qrcode.image import base
from ..tools.Logger import logger 
from pydantic import BaseModel
from app.tools.token import getCID
from .login import User
from app import routers
from ..DataBase.customerDB import query,insert, queryAll,queryByCID,deleteByCID
from ..core.aliveList import *
from ..core.aliveList import aliveVerify
from traceback import format_exc
import qrcode
from fastapi.responses import FileResponse,JSONResponse
import base64


class customer(BaseModel):
    CID:Optional[str]
    CName:Optional[str]
    addres:Optional[str]
    phone:Optional[str]
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
    if input.CID == None:
        input.CID=getCID()
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
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'msg':'wrong info'})
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'msg':'wrong token'})
    
@router.post('/getCostInfo')
def getCostInfo(input:userVerify):
    token=input.token
    UID=input.UID
    if token == None or UID == None :
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'msg':'permission denied'})
    if aliveVerify('admin',token) or aliveVerify(UID,token):
        try:
            if UID=='admin':
                List=queryAll(UID)
            else:
                List=query(UID)
        except Exception as e:
            raise e
        ret={}
        for p,info in enumerate(List):
            if len(info)==4:
                ret.update({
                    str(p):{
                        'CID':info[0],
                        'CName':info[1],
                        'addres':info[2],
                        'phone':info[3],
                    }
                })
            else:
                ret.update({
                    str(p):{
                        'CID':info[0],
                        'CName':info[1],
                        'addres':info[2],
                        'phone':info[3],
                        'UID':info[4],
                    }
                })
        return ret
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'msg':'wrong token'})

@router.post('/getCostInfoAll')
def getCostInfoAll(input:userVerify):
    token=input.token
    UID=input.UID
    if token == None or UID == None :
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'msg':'permission denied'})
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
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'msg':'wrong token'})
            
@router.get('/getQR')
def getQR(UID:str,CID:str,token:str):
    if CID == None or token == None or UID != 'admin':
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'msg':'permission denied'})
    if aliveVerify(UID,token):
        try:
            List=queryByCID(CID)
        except Exception as e:
            raise e
        info=List[0]
        ret={}
        ret.update({
            'CID':info[0],
            'CName':info[1],
            'addres':info[2],
            'phone':info[3],
        })
        ret=str(ret).encode()
        ret=base64.b64encode(ret).decode()
        logger.info("UID:{} | ret:{}".format(CID,ret))
        img=qrcode.make(ret)
        imgPath='./data/{}_qrcode.png'.format(CID)
        with open(imgPath,'wb') as f:
            img.save(f)
        return FileResponse(path=imgPath,filename=imgPath.split('/')[2])
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'msg':'wrong token'})


@router.get('/deleteByCID')
def delByCID(UID:str,CID:str,token:str):
    if CID == None or token == None or UID != 'admin':
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'msg':'permission denied'})
    if aliveVerify(UID,token):
        try:
            deleteByCID(CID)
        except Exception as e:
            raise e
        return {'msg':'info deleted'}
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={'msg':'wrong token'})

