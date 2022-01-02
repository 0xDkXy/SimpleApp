from fastapi import APIRouter
from pydantic import BaseModel

from app import routers
from ..DataBase.customerDB import query,insert

class customer(BaseModel):
    CID:str
    CName:str
    addres:str
    phone:str

router=APIRouter(
    prefix='/user',
    tags=['customer'],
    responses={404:{'description':'Not found'}},
)

@router.post('/{}')
def test():
    pass