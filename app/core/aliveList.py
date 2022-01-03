__all__=['aliveUpdate','aliveDelete','aliveClear']
from time import time


class Alive:
    '''
    半小时后超时
    '''
    def __init__(self) -> None:
        self.__Alive={}

    def update(self,new:dict)->None:
        self.__Alive.update(**new)
        self.__timeout()

    def clear(self)->None:
        self.__Alive.clear()
        self.__timeout()

    def logout(self,UID:str)->None:
        self.__delete(UID)
        self.__timeout()

    def verify(self,UID:str,token:str)->None:
        self.__timeout()
        try:
            if self.__Alive[UID]==token:
                return True
            else:
                return False
        except:
            return False

    def __delete(self,UID:str)->None:
        self.__Alive.pop(UID)

    def __isAlive(self,startTime:int)->bool:
        now=int(time())
        # self.__timeout()
        return False if now-startTime >= 1800 else True

    def __timeout(self):
        for user in self.__Alive.copy():
            # _=int(self.__Alive[user][16:])
            # print(_)
            if not self.__isAlive(int(self.__Alive[user][16:])):
                self.delete(user)
    
AliveList=Alive()

def aliveUpdate(new:dict)->None:
    AliveList.update(new)

def aliveClear()->None:
    AliveList.clear();

def aliveDelete(UID:str,token:str)->None:
    if aliveVerify(UID,token):
        AliveList.logout(UID)

def aliveVerify(UID:str,token:str)->bool:
    return AliveList.verify(UID,token);

