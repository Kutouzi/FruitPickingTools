import httpx

import Util as ut

def randomIDSet(hiatusID:str):
    idSet:set = set()
    for randomFileID1 in range(65,90+1):
        for randomFileID2 in range(48,57+1):
            temp:str = hiatusID+"E"+chr(randomFileID1)+chr(randomFileID2)
            idSet.add(temp)
    for randomFileID1 in range(48,57+1):
        for randomFileID2 in range(65,90+1):
            temp:str = hiatusID+"E"+chr(randomFileID1)+chr(randomFileID2)
            idSet.add(temp)
    for randomFileID1 in range(48,57+1):
        for randomFileID2 in range(48,57+1):
            temp:str = hiatusID+"E"+chr(randomFileID1)+chr(randomFileID2)
            idSet.add(temp)
    for randomFileID1 in range(65,90+1):
        for randomFileID2 in range(65,90+1):
            temp:str = hiatusID+"E"+chr(randomFileID1)+chr(randomFileID2)
            idSet.add(temp)
    return idSet

def getURL(randomIDSet:set):
    flag = True
    url=r"http://fruful.jp/img/game/chara/graphic/"
    while(flag):
        if randomIDSet.__len__()>0:
            try:
                tmp = randomIDSet.pop()
                data = httpx.get(url + tmp + "/icon/" + tmp + ".png",timeout=5)
                if data.status_code == 200:
                    return tmp
                # else:
                #     print("no find")
            except:
                print("time out")
        else:
            break
    return ''
