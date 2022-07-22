from concurrent.futures import ThreadPoolExecutor

import Util
import GetCG
import threading

is_40_ok:bool = False
is_100_ok:bool = False

lock = threading.Lock()

def traversCG(tables):
    defURL = r"http://fruful.jp/img/game/chara/event"
    TRAVERSE_MODE:bool = True
    randomCodeSet:set = set()
    for it in Util.yield_str():
        randomCodeSet.add(it)
    if TRAVERSE_MODE:
        with ThreadPoolExecutor(max_workers=100) as pool:
            pool.submit(traverseMode,kwargs={"tables":tables,"randomCodeSet":randomCodeSet,"TRAVERSE_MODE":TRAVERSE_MODE,"defURL":defURL})
    else:
        noTraverseMode(tables,TRAVERSE_MODE,defURL)

def noTraverseMode(tables,TRAVERSE_MODE:bool,defURL:str):
    OutputSet = Util.traverseOutputFile("./output")
    for index,row in tables.iterrows():
        randomCode = row['randomCode']
        charaID = row['charaID']
        charaFileID = row['charaFileID']
        if charaID not in OutputSet:
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

def traverseMode(tables,randomCodeSet,TRAVERSE_MODE:bool,defURL):
    for index,row in tables.iterrows():
        global is_40_ok
        global is_100_ok
        randomCode = ''
        charaID = row['charaID']
        charaFileID = row['charaFileID']
        if row['favorability'] == '' and row['randomCode'] == '':
            lock.acquire()
            randomCodeSet.pop()
            lock.release()
            print("begin find " + charaID)
            while(1):
                if not is_40_ok :
                    if Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID, randomCode,TRAVERSE_MODE, favorability="040", isOldCg=False)) == 0:
                        lock.acquire()
                        is_40_ok = True
                        lock.release()
                if not is_100_ok :
                    lock.acquire()
                    if Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID, randomCode,TRAVERSE_MODE, favorability="100", isOldCg=False)) == 0:
                        is_100_ok = True
                        lock.release()
                if is_40_ok and is_100_ok:
                    print("40 and 100 has find and save to files")
                    break


