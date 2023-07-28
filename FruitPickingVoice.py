import os

from pathlib import Path
import pandas as pd
import httpx
from more_itertools import chunked
from loguru import logger
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

logger.add('./logs/FruitPickingVoiceLog_{time}.log', format="{name} {level} {message}", level="DEBUG", rotation='5 MB', encoding='utf-8')


def yieldCharaSet(charaSet):
    while charaSet:
        yield charaSet.pop()

def requestURL(headURL,retryCount,chara,TRAVERSE_EVENT):
    maxArray = list(range(1,101))
    for arr in maxArray:
        for _ in range(retryCount):
            try:
                if TRAVERSE_EVENT:
                    voiceName = f'{arr:03d}' + ".m4a"
                    data = httpx.get(headURL + chara+'/voice/'+voiceName,timeout=5)
                else:
                    voiceName = "S" + f'{arr:03d}' + ".m4a"
                    data = httpx.get(headURL + chara+'/'+voiceName,timeout=5)
                if data.status_code == 200:
                    voice = data.content
                    if TRAVERSE_EVENT:
                        saveResource(voice,voiceName,Path("./outputv/"),chara,TRAVERSE_EVENT)
                    else:
                        saveResource(voice,voiceName,Path("./outputnv/"),chara,TRAVERSE_EVENT)
                    break
                if data.status_code == 403:
                    logger.warning("not found resource at " + voiceName)
                    return
            except:
                logger.warning(f"charactor: {chara[:7]} at {arr}, request timeout, {_ + 1} retry")

def saveResource(voice,voiceName:str,path:Path,chara:str,TRAVERSE_EVENT):
    if TRAVERSE_EVENT:
        path = (path / (chara[:7]) / (chara[7:]) / Path('voice'))
    else:
        path = (path / chara )
    try:
        path.mkdir(parents=True,exist_ok=True)
    except:
        logger.error("error creating directory: " + path.__str__())
    try:
        temp = path / voiceName
        temp.write_bytes(voice)
        logger.info("resource have been saved")
    except:
        logger.error("error writing to file: " + voiceName)

if __name__ == '__main__':
    if os.path.exists("./outputv") and os.path.exists("./outputnv"):
        pass
    else:
        try:
            os.mkdir("./outputv")
            os.mkdir("./outputnv")
        except:
            logger.error("cant create directory. please check permissions.")
            exit(-1)

    #初始化变量
    retryCount = 12
    TRAVERSE_EVENT = True
    OutputSet = set()

    tables = pd.read_csv("./charaMap/charaData.csv",
                         converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})

    if TRAVERSE_EVENT == True:
        headURL = 'http://fruful.jp/img/game/chara/event/'
        for root, dirs, files in os.walk('./outputv/',topdown=False):
            OutputSet.add(root[10:13])
        OutputSet.remove('')
        charaSet = set()
        for index,row in tables.iterrows():
            if not row['charaID'] in OutputSet and not row['favorability'] == '0' and not row['favorability'] == '':
                if row['randomCode'].__len__() > 5:
                    charaSet.add(row['charaID'] + row['charaFileID'] + '/' + row['favorability']+row['randomCode']+"_R")
                else:
                    charaSet.add(row['charaID'] + row['charaFileID'] + '/'+ row['favorability']+row['randomCode']+row['charaID']+"_R")
        with ThreadPoolExecutor(max_workers=100) as pool:
            for chunk in chunked(yieldCharaSet(charaSet),25):
                futures = []
                for chara in chunk:
                    pool.submit(requestURL,headURL,retryCount,chara,TRAVERSE_EVENT)
                list(concurrent.futures.as_completed(futures))
    else:
        headURL = 'http://fruful.jp/img/game/chara/voice/'
        for root, dirs, files in os.walk('./outputnv/',topdown=False):
            OutputSet.add(root[10:13])
        OutputSet.remove('')
        charaSet = set()
        for index,row in tables.iterrows():
            if not row['charaID'] in OutputSet and not row['favorability'] == '0' and not row['favorability'] == '':
                charaSet.add(row['charaID'] + row['charaFileID'])
        with ThreadPoolExecutor(max_workers=50) as pool:
            for chunk in chunked(yieldCharaSet(charaSet),25):
                futures = []
                for chara in chunk:
                    pool.submit(requestURL,headURL,retryCount,chara,TRAVERSE_EVENT)
                list(concurrent.futures.as_completed(futures))