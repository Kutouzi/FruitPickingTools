import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

from more_itertools import chunked

import Util
import GetCG
import threading
from loguru import logger

logger.add('./logs/traverslog_{time}.log', format="{name} {level} {message}", level="DEBUG", rotation='5 MB', encoding='utf-8')

charaDict = {'is_40_ok':False,'is_100_ok':False}

lock = threading.Lock()

def traversCG(tables, startRandomCode:str, TRAVERSE_MODE:bool, specifyCharaID:str, specifyCharaFileID:str, specifyFavorability:str, retryCount:int, silentMode:bool):
    defURL = r"http://fruful.jp/img/game/chara/event"
    if startRandomCode != '':
        argList=[ord(x) for x in list(startRandomCode.upper())]
    else:
        argList=list()
    # randomCodeSet:set = set()
    # for it in Util.yield_str():
    #     randomCodeSet.add(it)
    if TRAVERSE_MODE:
        if specifyCharaID == '' and specifyCharaFileID == '':
            with ThreadPoolExecutor(max_workers=100) as pool:
                for index,row in tables.iterrows():
                    charaDict['is_40_ok'] = False
                    charaDict['is_100_ok'] = False
                    charaID = row['charaID']
                    charaFileID = row['charaFileID']
                    if row['favorability'] == '' and row['randomCode'] == '':
                        for chunk in chunked(Util.yield_str(argList),1000):
                            futures = []
                            for randomCode in chunk:
                                futures.append(
                                    pool.submit(traverseMode, charaID, charaFileID, randomCode, TRAVERSE_MODE, defURL, retryCount, silentMode)
                                )
                            list(concurrent.futures.as_completed(futures))
                            if charaDict.get("is_40_ok") and charaDict.get("is_100_ok"):
                                logger.info("all tasks have been completed and saved to file")
                                break
        else:
            with ThreadPoolExecutor(max_workers=100) as pool:
                charaDict['is_40_ok'] = False
                charaDict['is_100_ok'] = False
                if specifyFavorability == '040':
                    charaDict['is_100_ok'] = True
                if specifyFavorability == '100':
                    charaDict['is_40_ok'] = True
                for chunk in chunked(Util.yield_str(argList),1000):
                    futures = []
                    for randomCode in chunk:
                        futures.append(
                            pool.submit(traverseMode, specifyCharaID, specifyCharaFileID, randomCode, TRAVERSE_MODE, defURL, retryCount, silentMode)
                        )
                    list(concurrent.futures.as_completed(futures))
                    if charaDict.get("is_40_ok") and charaDict.get("is_100_ok"):
                        logger.info("all tasks have been completed and saved to file")
                        break
    else:
        noTraverseMode(tables, TRAVERSE_MODE, defURL, retryCount, silentMode)

def noTraverseMode(tables, TRAVERSE_MODE:bool, defURL:str, retryCount:int, silentMode:bool):
    OutputSet = Util.traverseOutputFile("./output")
    for index,row in tables.iterrows():
        randomCode = row['randomCode']
        charaID = row['charaID']
        charaFileID = row['charaFileID']
        if charaID in OutputSet:
            logger.warning(charaID + r" data has exist in ./output")
            continue
        if row['favorability'] != '' and randomCode != '':
            if randomCode.__len__() == 4:
                if not Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID, randomCode, TRAVERSE_MODE, retryCount, silentMode, row["favorability"], isOldCg=False)):
                    logger.info("favorability:" + row['favorability'] + ", charaID:"+charaID + ", Hscene have been saved" )
            elif randomCode.__len__() == 7:
                if not Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID, randomCode, TRAVERSE_MODE, retryCount, silentMode, row["favorability"], isOldCg=True)):
                    logger.info("favorability:" + row['favorability'] + ", charaID:"+charaID + ", Hscene have been saved")
        elif row['favorability'] == '0' and randomCode == '0':
            logger.info("this character does not have a cg")

def traverseMode(charaID, charaFileID, randomCode, TRAVERSE_MODE:bool, defURL, retryCount:int, silentMode:bool):
            # lock.acquire()
            # randomCode = randomCodeSet.pop()
            # lock.release()
            # print("begin find " + charaID)
            if not charaDict.get("is_40_ok") :
                if Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID,
                                                   randomCode, TRAVERSE_MODE, retryCount, silentMode, favorability="040", isOldCg=False)) == 0:
                    lock.acquire()
                    charaDict['is_40_ok'] = True
                    lock.release()
            if not charaDict.get("is_100_ok") :
                if Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID,
                                                   randomCode, TRAVERSE_MODE, retryCount, silentMode, favorability="100", isOldCg=False)) == 0:
                    lock.acquire()
                    charaDict['is_100_ok'] = True
                    lock.release()



