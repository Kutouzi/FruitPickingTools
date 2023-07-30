
import os
from pathlib import Path
import pandas as pd
import httpx
from more_itertools import chunked
from loguru import logger
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

logger.add('./logs/FruitPickingBokkoLog_{time}.log', format="{name} {level} {message}", level="DEBUG", rotation='5 MB', encoding='utf-8')

def requestURL(chara:str,retryCount:int):
    bokkoURL='http://fruful.jp/img/game/asset/fullbokko/'
    for _ in range(retryCount):
        try:
            resourceName = chara + ".png"
            pngURL = bokkoURL + resourceName
            png = httpx.get(pngURL,timeout=5)
            if png.status_code == 200:
                resource = png.content
                saveResource(resource,resourceName,Path("./outputbo/"))
                break
            if png.status_code == 403:
                logger.warning("not found json resource at " + chara)
                break
        except:
            logger.warning(f"resource: {chara}.png, request timeout, {_ + 1} retry")

def saveResource(resource,resourceName:str,path:Path):
    try:
        path.mkdir(parents=True,exist_ok=True)
    except:
        logger.error("error creating directory: " + path.__str__())
    try:
        (path / (resourceName)).write_bytes(resource)
        logger.info("resource have been saved")
    except:
        logger.error("error writing to file: " + resourceName)

def yieldCharaSet(charaSet):
    while charaSet:
        yield charaSet.pop()

if __name__ == '__main__':
    if os.path.exists("./outputbo"):
        pass
    else:
        try:
            os.mkdir("./outputbo")
        except:
            logger.error("cant create directory. please check permissions.")
            exit(-1)
    tables = pd.read_csv("./charaMap/charaData.csv",
                         converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    OutputSet = set()
    retryCount = 6
    for root, dirs, files in os.walk('./outputbo/',topdown=False):
        if files.__len__() > 0:
            for f in files:
                OutputSet.add(f[:3])
        else:
            break
    if OutputSet.__len__() > 0 :
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
                pool.submit(requestURL,chara,retryCount)
            list(concurrent.futures.as_completed(futures))


