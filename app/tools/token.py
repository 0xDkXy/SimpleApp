import re
from time import time
from random import randint
from hashlib import sha256

def getToken()->str:
    encry=sha256()
    encry.update(str(randint(0,19999999)).encode())
    tmpToken=encry.hexdigest()[:16]
    now=str(int(time()))
    del encry
    return tmpToken+now

def getCID()->str:
    encry=sha256()
    encry.update(str(int(time())).encode())
    ret=encry.hexdigest()
    del encry
    return ret

