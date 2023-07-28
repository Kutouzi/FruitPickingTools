import os

from pathlib import Path
import pandas as pd
import httpx
from more_itertools import chunked
from loguru import logger
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

logger.add('./logs/FruitPickingEventLog_{time}.log', format="{name} {level} {message}", level="DEBUG", rotation='5 MB', encoding='utf-8')


def yieldCharaSet(charaSet):
    while charaSet:
        yield charaSet.pop()

def requestURL(headURL,retryCount,chara):
    for _ in range(retryCount):
        try:
            dataName = 'data.txt'
            data = httpx.get(headURL + chara+'/'+dataName,timeout=5)
            if data.status_code == 200:
                txt = data.content
                saveResource(txt,dataName,Path("./outpute/"),chara)
                break
            if data.status_code == 403:
                logger.warning("not found resource at " + chara)
                return
        except:
            logger.warning(f"charactor: {chara} , request timeout, {_ + 1} retry")

def saveResource(txt,dataName:str,path:Path,chara:str):
    path = (path / (chara[:7]) / (chara[7:]))
    try:
        path.mkdir(parents=True,exist_ok=True)
    except:
        logger.error("error creating directory: " + path.__str__())
    try:
        temp = path / dataName
        temp.write_bytes(txt)
        logger.info("resource have been saved")
    except:
        logger.error("error writing to file: " + dataName)

if __name__ == '__main__':
    if os.path.exists("./outpute"):
        pass
    else:
        try:
            os.mkdir("./outpute")
        except:
            logger.error("cant create directory. please check permissions.")
            exit(-1)

    #初始化变量
    retryCount = 12
    tables = pd.read_csv("./charaMap/charaData.csv",
                         converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    headURL = 'http://fruful.jp/img/game/chara/event/'
    charaSet = set()
    OutputSet = set()
    for root, dirs, files in os.walk('./outpute/',topdown=False):
        OutputSet.add(root[10:13])
    OutputSet.remove('')
    for index,row in tables.iterrows():
        if not row['charaID'] in OutputSet and not row['favorability'] == '0' and not row['favorability'] == '':
            if row['randomCode'].__len__() > 5:
                charaSet.add(row['charaID'] + row['charaFileID'] + '/' + row['favorability']+row['randomCode']+"_R")
            else:
                charaSet.add(row['charaID'] + row['charaFileID'] + '/'+ row['favorability']+row['randomCode']+row['charaID']+"_R")
    with ThreadPoolExecutor(max_workers=50) as pool:
        for chunk in chunked(yieldCharaSet(charaSet),25):
            futures = []
            for chara in chunk:
                pool.submit(requestURL,headURL,retryCount,chara)
            list(concurrent.futures.as_completed(futures))