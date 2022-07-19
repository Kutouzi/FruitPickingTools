import httpx

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
    print("test id: " + hiatusID + ";" + "random len: " + idSet.__len__().__str__())
    return idSet

def getURL(randomIDSet:set):
    url=r"http://fruful.jp/img/game/chara/graphic/"
    while(1):
        if randomIDSet.__len__()>0:
            tmp = randomIDSet.pop()
            try:
                data = httpx.get(url + tmp + "/icon/" + tmp + ".png",timeout=5)
                if data.status_code == 200:
                    # print(tmp + " has find")
                    return tmp
                # else:
                    # print(tmp + " no find")
            except:
                print(tmp + " time out 1")
                try:
                    data = httpx.get(url + tmp + "/icon/" + tmp + ".png",timeout=5)
                    if data.status_code == 200:
                        return tmp
                except:
                    print(tmp + " time out 2")
                    try:
                        data = httpx.get(url + tmp + "/icon/" + tmp + ".png",timeout=5)
                        if data.status_code == 200:
                            return tmp
                    except:
                        print(tmp + " time out 3")
        else:
            break
    return ''
