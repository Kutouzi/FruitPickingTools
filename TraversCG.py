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

def traversCG(tables,TRAVERSE_MODE:bool,specifyCharaID:str,specifyCharaFileID:str):
    defURL = r"http://fruful.jp/img/game/chara/event"
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
                        for chunk in chunked(Util.yield_str(),1000):
                            futures = []
                            for randomCode in chunk:
                                futures.append(
                                    pool.submit(traverseMode,charaID,charaFileID,randomCode,TRAVERSE_MODE,defURL)
                                )
                            list(concurrent.futures.as_completed(futures))
                            if charaDict.get("is_40_ok") and charaDict.get("is_100_ok"):
                                logger.info("40 and 100 has find and save to files")
                                break
        else:
            with ThreadPoolExecutor(max_workers=100) as pool:
                    charaDict['is_40_ok'] = False
                    charaDict['is_100_ok'] = False
                    for chunk in chunked(Util.yield_str(),10):
                        futures = []
                        for randomCode in chunk:
                            futures.append(
                                pool.submit(traverseMode,specifyCharaID,specifyCharaFileID,randomCode,TRAVERSE_MODE,defURL)
                            )
                        list(concurrent.futures.as_completed(futures))
                        if charaDict.get("is_40_ok") and charaDict.get("is_100_ok"):
                            logger.info("40 and 100 has find and save to files")
                            break
    else:
        noTraverseMode(tables,TRAVERSE_MODE,defURL)

def noTraverseMode(tables,TRAVERSE_MODE:bool,defURL:str):
    OutputSet = Util.traverseOutputFile("./output")
    for index,row in tables.iterrows():
        randomCode = row['randomCode']
        charaID = row['charaID']
        charaFileID = row['charaFileID']
        if charaID in OutputSet:
            print(charaID + r" data has exist in ./output")
            continue
        if row['favorability'] != '' and randomCode != '':
            if randomCode.__len__() == 4:
                if not Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID, randomCode,TRAVERSE_MODE, row["favorability"], isOldCg=False)):
                    print("finish save " + row['favorability'] + " favorability cg" + charaID)
            elif randomCode.__len__() == 7:
                if not Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID, randomCode,TRAVERSE_MODE, row["favorability"], isOldCg=True)):
                    print("finish save " + row["favorability"] +" favorability cg" + charaID)
        elif row['favorability'] == '0' and randomCode == '0':
            print("the chara no have cg")

def traverseMode(charaID,charaFileID,randomCode,TRAVERSE_MODE:bool,defURL):
            # lock.acquire()
            # randomCode = randomCodeSet.pop()
            # lock.release()
            # print("begin find " + charaID)
            if not charaDict.get("is_40_ok") :
                if Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID,
                                                   randomCode,TRAVERSE_MODE, favorability="040", isOldCg=False)) == 0:
                    lock.acquire()
                    charaDict['is_40_ok'] = True
                    lock.release()
            if not charaDict.get("is_100_ok") :
                if Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID,
                                                   randomCode,TRAVERSE_MODE, favorability="100", isOldCg=False)) == 0:
                    lock.acquire()
                    charaDict['is_100_ok'] = True
                    lock.release()



