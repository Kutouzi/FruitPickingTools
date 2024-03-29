import os
import threading
import FruitPickingWeapons
from pathlib import Path
import pandas as pd
import httpx
from more_itertools import chunked
from loguru import logger
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

logger.add('./logs/FruitPickingWeaponsLog_{time}.log', format="{name} {level} {message}", level="DEBUG", rotation='5 MB', encoding='utf-8')

lock = threading.Lock()
foundFlag = False

def yieldHashCode(hashCodeSet):
    while hashCodeSet:
        yield hashCodeSet.pop()

def checkInfo(idBeginRange:int,idEndRange:int,table,otherTable):
    numList:set = set(range(idBeginRange,idEndRange+1))
    IDTable:set = set()
    IDOtherTable:set = set()
    for index,row in table.iterrows():
        a = int(row['weaponID'])
        IDTable.add(a)
    for index,row in otherTable.iterrows():
        a = int(row['weaponID'])
        IDOtherTable.add(a)
    resultSet = (set(numList) - set(IDTable)) - set(IDOtherTable)
    return resultSet

def testURL(headURL:str,tableIdentity:str,hashCode:str,id:str,retryCount:int,tables,otherTables):
    for _ in range(retryCount):
        try:
            imageName = tableIdentity + id + hashCode + ".png"
            data = httpx.get(headURL + imageName,timeout=5)
            if data.status_code == 200:
                lock.acquire()
                FruitPickingWeapons.foundFlag = True
                image = data.content
                saveResource(image,imageName,Path("./outputwp/"))
                insertTable(tableIdentity,id,hashCode,tables)
                lock.release()
                return id+hashCode
            if data.status_code == 403:
                #
                if tableIdentity == 'C':
                    antiTableIdentity = 'W'
                else:
                    antiTableIdentity = 'C'
                imageName = antiTableIdentity + id + hashCode + ".png"
                data = httpx.get(headURL + imageName,timeout=5)
                if data.status_code == 200:
                    lock.acquire()
                    FruitPickingWeapons.foundFlag = True
                    image = data.content
                    saveResource(image,imageName,Path("./outputwp/"))
                    insertTable(antiTableIdentity,id,hashCode,otherTables)
                    lock.release()
                    return id+hashCode
                if data.status_code == 403:
                    #logger.warning("not found hashCode at " + id +hashCode)
                    break
        except:
            logger.warning(f"tableIdentity: {tableIdentity} and hashCode:{hashCode}, request timeout, {_ + 1} retry")
    return ''

def requestURL(headURL:str,tableIdentity:str,weaponID:str,hashCode:str,retryCount:int):
    for _ in range(retryCount):
        try:
            imageName = tableIdentity + weaponID + hashCode + ".png"
            data = httpx.get(headURL + imageName,timeout=5)
            if data.status_code == 200:
                image = data.content
                saveResource(image,imageName,Path("./outputwpf/"))
                break
            if data.status_code == 403:
                logger.warning("not found resource at " + hashCode)
                break
        except:
            logger.warning(f"tableIdentity: {tableIdentity} and hashCode:{hashCode}, request timeout, {_ + 1} retry")

def hashCodeSetConstructor1000(hiatusID:str):
    codeSet:set = set()
    for randomFileID1 in range(65,90+1):
            temp:str = hiatusID+chr(randomFileID1)
            codeSet.add(temp)
    return codeSet

def hashCodeSetConstructor(hiatusID:str):
    codeSet:set = set()
    for randomFileID1 in range(65,90+1):
        for randomFileID2 in range(65,90+1):
            temp:str = hiatusID+chr(randomFileID1)+chr(randomFileID2)
            codeSet.add(temp)
    return codeSet

def insertTable(tableIdentity,weaponID,hashCode,table):
    #'identity':str,'weaponID':str,'hashCode':str
    for index,row in table.iterrows():
        if  row['weaponID'] == weaponID and row['hashCode'] == '':
            row.at['hashCode'] = hashCode
            updateTable(tableIdentity,table)
            return
        elif row['weaponID'] == '' and row['hashCode'] == '':
            row.at['weaponID'] = weaponID
            row.at['hashCode'] = hashCode
            updateTable(tableIdentity,table)
            return
    table.loc[table.__len__()+2] = [tableIdentity,weaponID,hashCode]
    updateTable(tableIdentity,table)

def updateTable(tableIdentity,table):
    resultTable = table.sort_values(by='weaponID',ascending=True)
    csvStr = "./weaponMap/weaponData_" + tableIdentity + ".csv"
    resultTable.to_csv(csvStr,index=False)
    logger.info(csvStr + " table updated")

def loopFunciton(hashCode,headURL,tableIdentity,id,retryCount,tables,otherTables):
    lock.acquire()
    flag = FruitPickingWeapons.foundFlag
    lock.release()
    if flag == False :
        hashCodeString = testURL(headURL,tableIdentity,hashCode,id,retryCount,tables,otherTables)
        if hashCodeString == '':
            pass
        else:
            logger.info("found hashCode is "+ hashCodeString + " at " + hashCode)

def saveResource(image,imageName:str,path:Path):
    try:
        path.mkdir(parents=True,exist_ok=True)
    except:
        logger.error("error creating directory: " + path.__str__())
    try:
        (path / (imageName)).write_bytes(image)
        logger.info("resource have been saved")
    except:
        logger.error("error writing to file: " + imageName)

def traverseOutputFile(path:str):
    aList = []
    for root, dirs, files in os.walk(path,topdown=False):
        aList.append(files)
    return set(aList.pop())

if __name__ == '__main__':
    #创建输出图像的文件夹
    if os.path.exists("./outputwp") and os.path.exists("./var") and os.path.exists("./outputwpf"):
        pass
    else:
        try:
            os.mkdir("./outputwp")
            os.mkdir("./outputwpf")
            os.mkdir("./var")
        except:
            logger.error("cant create directory. please check permissions.")
            exit(-1)

    varTables = pd.read_csv("./var/weapon_var.csv",converters={'var':str,'value':str})

    #初始化变量
    idBeginRange = 1
    idEndRange = 999
    retryCount = 6
    randomList = []
    headURL = 'http://fruful.jp/img/game/asset/equip/icon/'
    tableIdentity = ''
    identity =''
    weaponID =''
    hashCode =''
    tables=''
    TRAVERSE_MODE:bool = False
    #读取配置文件
    for index,row in varTables.iterrows():
        if row['var'] == 'TRAVERSE_MODE':
            TRAVERSE_MODE = bool(int(row['value']))
        if row['var'] == 'idBeginRange':
            idBeginRange = int(row['value'])
        if row['var'] == 'idEndRange':
            idEndRange = int(row['value'])
        if row['var'] == 'tableIdentity':
            tableIdentity = row['value']
        if row['var'] == 'retryCount':
            retryCount = int(row['value'])
    #验证配置文件合法性
    if not tableIdentity == 'C' and not tableIdentity == 'W':
        logger.error("config file './var/weaponVar.csv' have a error tableIdentity. only allowed 'C' or 'W'.")
        exit(-1)
    if idBeginRange <= 0 :
        logger.error("config file './var/weaponVar.csv' idBeginRange wrong value.")
        exit(-1)
    if idEndRange <= 0 :
        logger.error("config file './var/weaponVar.csv' idEndRange wrong value.")
        exit(-1)
    if retryCount <=0 :
        logger.warning("config file './var/weaponVar.csv' retryCount value too is too small. Has been reset to default.")
        retryCount = 6

    if TRAVERSE_MODE:
        #创建表格，并读取内容
        tablesC = pd.read_csv("./weaponMap/weaponData_C.csv",
                              converters={'identity':str,'weaponID':str,'hashCode':str})
        tablesW = pd.read_csv("./weaponMap/weaponData_W.csv",
                              converters={'identity':str,'weaponID':str,'hashCode':str})
        otherTables = ''
        hiatusTable = ''
        if tableIdentity == 'C':
            tables = pd.read_csv("./weaponMap/weaponData_C.csv",
                                 converters={'identity':str,'weaponID':str,'hashCode':str})
            #由于双表是互补的，因此还需要让对表做差
            hiatusTable = checkInfo(idBeginRange,idEndRange,tables,tablesW)
            otherTables = tablesW
        if tableIdentity == 'W':
            tables = pd.read_csv("./weaponMap/weaponData_W.csv",
                                 converters={'identity':str,'weaponID':str,'hashCode':str})
            hiatusTable = checkInfo(idBeginRange,idEndRange,tables,tablesC)
            otherTables = tablesC

        logger.info("The number of missing IDs is " + hiatusTable.__len__().__str__())
        #判断标识符进行操作
        if tableIdentity == 'C' or tableIdentity == 'W':
            while hiatusTable.__len__():
                id = hiatusTable.pop()
                sid = ''
                if id >= 1000:
                    sid = f'{id:04d}'
                    hashCodeSet = hashCodeSetConstructor1000('')
                else:
                    sid = f'{id:03d}'
                    hashCodeSet = hashCodeSetConstructor('')
                logger.info('now is ' + sid)
                with ThreadPoolExecutor(max_workers=100) as pool:
                    for chunk in chunked(yieldHashCode(hashCodeSet),500):
                        futures = []
                        for hashCode in chunk:
                            futures.append(pool.submit(loopFunciton,hashCode,headURL,tableIdentity,sid,retryCount,tables,otherTables))
                        list(concurrent.futures.as_completed(futures))
                FruitPickingWeapons.foundFlag = False
        else:
            logger.error("config file './var/weaponVar.csv' have a error tableIdentity. only allowed 'C' or 'W'.")
            exit(-1)
    else:
        tablesC = pd.read_csv("./weaponMap/weaponData_C.csv",
                              converters={'identity':str,'weaponID':str,'hashCode':str})
        tablesW = pd.read_csv("./weaponMap/weaponData_W.csv",
                              converters={'identity':str,'weaponID':str,'hashCode':str})
        OutputSet = traverseOutputFile("./outputwpf/")
        idSet = set()
        relSet = set()
        for _ in OutputSet:
            idSet.add(_[1:4])
            if _[4:5].isdigit():
                idSet.add(_[1:5])
        for index,row in tablesC.iterrows():
            relSet.add(row['weaponID'])
        requestSetC = set(relSet) - set(idSet)
        relSet.clear()
        for index,row in tablesW.iterrows():
            relSet.add(row['weaponID'])
        requestSetW = set(relSet) - set(idSet)

        pool = ThreadPoolExecutor(max_workers=50)
        for index,row in tablesC.iterrows():
            if row['weaponID'] in requestSetC:
                pool.submit(requestURL,'http://fruful.jp/img/game/asset/equip/full/',row['identity'],row['weaponID'],row['hashCode'],retryCount)
        for index,row in tablesW.iterrows():
            if row['weaponID'] in requestSetW:
                pool.submit(requestURL,'http://fruful.jp/img/game/asset/equip/full/',row['identity'],row['weaponID'],row['hashCode'],retryCount)