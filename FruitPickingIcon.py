
import os
from pathlib import Path
import pandas as pd
import httpx
from more_itertools import chunked
from loguru import logger
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

logger.add('./logs/FruitPickingIconLog_{time}.log', format="{name} {level} {message}", level="DEBUG", rotation='5 MB', encoding='utf-8')

def requestURL(chara:str,retryCount:int,IsCharaIcon:bool):
    iconURL='http://fruful.jp/img/game/chara/graphic/'
    fruitsIconURL='http://fruful.jp/img/game/asset/fruitsicon/'
    if not IsCharaIcon:
        for _ in range(retryCount):
            try:
                resourceName = chara + ".png"
                fruitsIcon = httpx.get(fruitsIconURL + resourceName,timeout=5)
                if fruitsIcon.status_code == 200:
                    resource = fruitsIcon.content
                    saveResource(resource,resourceName,Path("./outputfic/"),Path(""),chara,IsCharaIcon)
                    break
                if fruitsIcon.status_code == 403:
                    logger.warning("not found resource at " + chara)
                    break
            except:
                logger.warning(f"charaName: {chara}, request timeout, {_ + 1} retry")
        return
    charaE = chara
    charaT = list(chara)
    charaT[3] = 'T'
    charaT = ''.join(charaT)
    for _ in range(retryCount):
        try:
            resourceName = charaE + ".png"
            iconURLE = iconURL + chara + '/icon/' + resourceName
            iconE = httpx.get(iconURLE,timeout=5)
            if iconE.status_code == 200:
                resource = iconE.content
                saveResource(resource,resourceName,Path("./outputic/"),Path("icon"),chara,IsCharaIcon)
                break
            if iconE.status_code == 403:
                logger.warning("not found resource at " + charaE)
                break
        except:
            logger.warning(f"charaName: {charaE}, request timeout, {_ + 1} retry")

    for _ in range(retryCount):
        try:
            resourceName = charaT + ".png"
            iconURLT = iconURL + chara + '/icon/' + resourceName
            iconT = httpx.get(iconURLT,timeout=5)
            if iconT.status_code == 200:
                resource = iconT.content
                saveResource(resource,resourceName,Path("./outputic/"),Path("icon"),chara,IsCharaIcon)
            if iconT.status_code == 403:
                logger.warning("not found resource at " + charaT)
                break
        except:
            logger.warning(f"charaName: {charaT}, request timeout, {_ + 1} retry")


def saveResource(resource,resourceName:str,path:Path,pathc:Path,chara:str,IsCharaIcon:bool):
    if IsCharaIcon:
        resultPath = path / Path(chara) /  pathc
    else:
        resultPath = path
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
    if os.path.exists("./outputic") and os.path.exists('./outputfic'):
        pass
    else:
        try:
            os.mkdir("./outputic")
            os.mkdir('./outputfic')
        except:
            logger.error("cant create directory. please check permissions.")
            exit(-1)
    tables = pd.read_csv("./charaMap/charaData.csv",
                         converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    OutputSet = set()
    retryCount = 6
    IsCharaIcon = True


    if IsCharaIcon :
        for root, dirs, files in os.walk('./outputic/',topdown=False):
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
                    pool.submit(requestURL,chara,retryCount,IsCharaIcon)
                list(concurrent.futures.as_completed(futures))
    else:
        for root, dirs, files in os.walk('./outputfic/',topdown=False):
            if files.__len__() > 0:
                for f in files:
                    OutputSet.add(f[:3])
            else:
                break
        if OutputSet.__len__() > 0:
            try:
                OutputSet.remove('')
            except:
                pass
        charaSet = set()
        for index,row in tables.iterrows():
            if not row['charaID'] in OutputSet and not row['favorability'] == '0' and not row['favorability'] == '':
                charaSet.add(row['charaID'] + row['charaFileID'])
        with ThreadPoolExecutor(max_workers=20) as pool:
            for chunk in chunked(yieldCharaSet(charaSet),20):
                futures = []
                for chara in chunk:
                    pool.submit(requestURL,chara,retryCount,IsCharaIcon)
                list(concurrent.futures.as_completed(futures))


