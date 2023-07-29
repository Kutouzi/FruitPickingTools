
import os
from pathlib import Path
import pandas as pd
import httpx
from more_itertools import chunked
from loguru import logger
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

logger.add('./logs/FruitPickingSpineLog_{time}.log', format="{name} {level} {message}", level="DEBUG", rotation='5 MB', encoding='utf-8')

def requestURL(chara:str,retryCount:int):
    spineURL='http://fruful.jp/img/game/spine/'
    for _ in range(retryCount):
        try:
            resourceName = 'skeleton' + ".json"
            jsonURL = spineURL + chara +'/'+ resourceName
            json = httpx.get(jsonURL,timeout=5)
            if json.status_code == 200:
                resource = json.content
                saveResource(resource,resourceName,Path("./outputsp/"),chara)
                break
            if json.status_code == 403:
                logger.warning("not found json resource at " + chara)
                break
        except:
            logger.warning(f"resource: {chara}.json, request timeout, {_ + 1} retry")

    for _ in range(retryCount):
        try:
            resourceName = 'skeleton' + ".atlas"
            atlasURL = spineURL + chara +'/'+ resourceName
            atlas = httpx.get(atlasURL,timeout=5)
            if atlas.status_code == 200:
                resource = atlas.content
                saveResource(resource,resourceName,Path("./outputsp/"),chara)
                break
            if atlas.status_code == 403:
                logger.warning("not found atlas resource at " + chara)
                break
        except:
            logger.warning(f"resource: {chara}.atlas, request timeout, {_ + 1} retry")

    for _ in range(retryCount):
        try:
            resourceName = 'skeleton' + ".png"
            pngURL = spineURL + chara +'/'+ resourceName
            png = httpx.get(pngURL,timeout=5)
            if png.status_code == 200:
                resource = png.content
                saveResource(resource,resourceName,Path("./outputsp/"),chara)
                break
            if png.status_code == 403:
                logger.warning("not found png resource at " + chara)
                break
        except:
            logger.warning(f"resource: {chara}.png, request timeout, {_ + 1} retry")


def saveResource(resource,resourceName:str,path:Path,chara:str):
    resultPath = path / Path(chara)
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
    if os.path.exists("./outputsp"):
        pass
    else:
        try:
            os.mkdir("./outputsp")
        except:
            logger.error("cant create directory. please check permissions.")
            exit(-1)
    tables = pd.read_csv("./charaMap/charaData.csv",
                         converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    OutputSet = set()
    retryCount = 6
    for root, dirs, files in os.walk('./outputsp/',topdown=False):
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


