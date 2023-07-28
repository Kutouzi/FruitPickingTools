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

logger.add('./logs/FruitPickingBattleLog_{time}.log', format="{name} {level} {message}", level="DEBUG", rotation='5 MB', encoding='utf-8')

def requestURL(chara:str,retryCount:int):
    #这个是战斗立绘
    commandURL='http://fruful.jp/img/game/chara/graphic/'
    #这个是技能立绘
    cutinURL='http://fruful.jp/img/game/chara/graphic/'
    charaE = chara
    charaT = list(chara)
    charaT[3] = 'T'
    charaT = ''.join(charaT)
    for _ in range(retryCount):
        try:
            resourceName = charaE + ".png"
            commandURLE = commandURL + chara + '/command/' + resourceName
            commandE = httpx.get(commandURLE,timeout=5)
            if commandE.status_code == 200:
                command = commandE.content
                saveResource(command,resourceName,Path("./outputbt/"),Path("command"),chara)
                break
            if commandE.status_code == 403:
                logger.warning("not found resource at " + charaE)
                break
        except:
            logger.warning(f"charaName: {charaE}, request timeout, {_ + 1} retry")

    for _ in range(retryCount):
        try:
            resourceName = charaT + ".png"
            commandURLT = commandURL + chara + '/command/' + resourceName
            commandT = httpx.get(commandURLT,timeout=5)
            if commandT.status_code == 200:
                command = commandT.content
                saveResource(command,resourceName,Path("./outputbt/"),Path("command"),chara)
            if commandT.status_code == 403:
                logger.warning("not found resource at " + charaT)
                break
        except:
            logger.warning(f"charaName: {charaT}, request timeout, {_ + 1} retry")

    for _ in range(retryCount):
        try:
            resourceName = charaE + '_E' + ".png"
            cutinURLE = cutinURL + chara + '/cutin/' + resourceName
            cutinE = httpx.get(cutinURLE,timeout=5)
            if cutinE.status_code == 200:
                cutin = cutinE.content
                saveResource(cutin,resourceName,Path("./outputbt/"),Path("cutin"),chara)
                break
            if cutinE.status_code == 403:
                logger.warning("not found resource at " + charaE)
                break
        except:
            logger.warning(f"tableIdentity: {charaE}, request timeout, {_ + 1} retry")

    for _ in range(retryCount):
        try:
            resourceName = charaT + '_T' + ".png"
            cutinURLT = cutinURL + chara + '/cutin/' + resourceName
            cutinT = httpx.get(cutinURLT,timeout=5)
            if cutinT.status_code == 200:
                cutin = cutinT.content
                saveResource(cutin,resourceName,Path("./outputbt/"),Path("cutin"),chara)
                break
            if cutinT.status_code == 403:
                logger.warning("not found resource at " + charaT)
                break
        except:
            logger.warning(f"tableIdentity: {charaT}, request timeout, {_ + 1} retry")

def saveResource(resource,resourceName:str,path:Path,pathc:Path,chara:str):
    resultPath = path / Path(chara) /  pathc
    try:
        resultPath.mkdir(parents=True,exist_ok=True)
    except:
        logger.error("error creating directory: " + resultPath.__str__())
    try:
        (resultPath / (resourceName)).write_bytes(resource)
        logger.info("resource have been saved")
    except:
        logger.error("error writing to file: " + resourceName)

def yieldCharaSet(charaSet):
    while charaSet:
        yield charaSet.pop()

if __name__ == '__main__':
    if os.path.exists("./outputbt"):
        pass
    else:
        try:
            os.mkdir("./outputbt")
        except:
            logger.error("cant create directory. please check permissions.")
            exit(-1)
    tables = pd.read_csv("./charaMap/charaData.csv",
                         converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    OutputSet = set()
    retryCount = 6
    for root, dirs, files in os.walk('./outputbt/',topdown=False):
        OutputSet.add(root[11:14])
    OutputSet.remove('')
    charaSet = set()
    for index,row in tables.iterrows():
        if not row['charaID'] in OutputSet and not row['favorability'] == '0' and not row['favorability'] == '':
            charaSet.add(row['charaID'] + row['charaFileID'])
    with ThreadPoolExecutor(max_workers=20) as pool:
        for chunk in chunked(yieldCharaSet(charaSet),20):
            futures = []
            for chara in chunk:
                pool.submit(requestURL,chara,retryCount)
            list(concurrent.futures.as_completed(futures))


