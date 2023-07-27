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

def checkInfo(idBeginRange:int,idEndRange:int,table):
    numList:set = set(range(idBeginRange,idEndRange+1))
    IDTable:set = set()
    for index,row in table.iterrows():
        a = int(row['weaponID'])
        IDTable.add(a)
    return set(numList) - set(IDTable)

def testURL(headURL:str,tableIdentity:str,hashCode:str,retryCount:int,tables):
    for _ in range(retryCount):
        try:
            imageName = tableIdentity + hashCode + ".png"
            data = httpx.get(headURL + imageName,timeout=5)
            if data.status_code == 200:
                lock.acquire()
                FruitPickingWeapons.foundFlag = True
                image = data.content
                saveResource(image,imageName,Path("./outputwp/"))
                insertTable(tableIdentity,hashCode,tables)
                lock.release()
                return hashCode
            if data.status_code == 403:
                #logger.warning("not found hashCode at " + hashCode)
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
            if data.status_code == 403:
                logger.warning("not found resource at " + hashCode)
                break
        except:
            logger.warning(f"tableIdentity: {tableIdentity} and hashCode:{hashCode}, request timeout, {_ + 1} retry")

def hashCodeSetConstructor(hiatusID:str):
    codeSet:set = set()
    for randomFileID1 in range(65,90+1):
        for randomFileID2 in range(48,57+1):
            temp:str = hiatusID+chr(randomFileID1)+chr(randomFileID2)
            codeSet.add(temp)
    for randomFileID1 in range(48,57+1):
        for randomFileID2 in range(65,90+1):
            temp:str = hiatusID+chr(randomFileID1)+chr(randomFileID2)
            codeSet.add(temp)
    for randomFileID1 in range(48,57+1):
        for randomFileID2 in range(48,57+1):
            temp:str = hiatusID+chr(randomFileID1)+chr(randomFileID2)
            codeSet.add(temp)
    for randomFileID1 in range(65,90+1):
        for randomFileID2 in range(65,90+1):
            temp:str = hiatusID+chr(randomFileID1)+chr(randomFileID2)
            codeSet.add(temp)
    return codeSet

def insertTable(tableIdentity,hashCodeString:str,table):
    #'identity':str,'weaponID':str,'hashCode':str
    weaponID = hashCodeString[0:3]
    hashCode = hashCodeString[3:]
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

def loopFunciton(hashCode,headURL,tableIdentity,retryCount,tables):
    lock.acquire()
    flag = FruitPickingWeapons.foundFlag
    lock.release()
    if flag == False :
        hashCodeString = testURL(headURL,tableIdentity,hashCode,retryCount,tables)
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
        if tableIdentity == 'C':
            tables = pd.read_csv("./weaponMap/weaponData_C.csv",
                                  converters={'identity':str,'weaponID':str,'hashCode':str})
        if tableIdentity == 'W':
            tables = pd.read_csv("./weaponMap/weaponData_W.csv",
                                  converters={'identity':str,'weaponID':str,'hashCode':str})

        hiatusTable = checkInfo(idBeginRange,idEndRange,tables)
        logger.info("The number of missing IDs is " + hiatusTable.__len__().__str__())
        #判断标识符进行操作
        if tableIdentity == 'C' or tableIdentity == 'W':
            while hiatusTable.__len__():
                temp = f'{hiatusTable.pop():03d}'
                logger.info('now is ' + temp)
                hashCodeSet = hashCodeSetConstructor(temp)
                with ThreadPoolExecutor(max_workers=100) as pool:
                    for chunk in chunked(yieldHashCode(hashCodeSet),500):
                        futures = []
                        for hashCode in chunk:
                            futures.append(pool.submit(loopFunciton,hashCode,headURL,tableIdentity,retryCount,tables))
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
        pool = ThreadPoolExecutor(max_workers=50)
        for index,row in tablesC.iterrows():
            pool.submit(requestURL,'http://fruful.jp/img/game/asset/equip/full/',row['identity'],row['weaponID'],row['hashCode'],retryCount)
        for index,row in tablesW.iterrows():
            pool.submit(requestURL,'http://fruful.jp/img/game/asset/equip/full/',row['identity'],row['weaponID'],row['hashCode'],retryCount)