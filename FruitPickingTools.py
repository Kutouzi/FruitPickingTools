import os
import pandas as pd
import GetCG
import Util

if __name__ == '__main__':
    defURL = r"http://fruful.jp/img/game/chara/event"
    checkCode = 1
    charaID:str = ''
    charaFileID:str = ""
    TRAVERSE_MODE:bool = True

    if os.path.exists("./output"):
        pass
    else:
        try:
            os.mkdir("./output")
        except:
            print(r"cant create directory './output'")
            exit(-1)

    tables = pd.read_csv("./charaMap/charaData.csv",
                converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    for index,row in tables.iterrows():
        is_40_ok:bool = False
        is_100_ok:bool = False
        randomCode = row['randomCode']
        charaID = row['charaID']
        charaFileID = row['charaFileID']
        if row['favorability'] == '' and randomCode == '' and TRAVERSE_MODE:
            print("begin find " + charaID)
            for randomCode in Util.yield_str():
                if not is_40_ok :
                    if Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID, randomCode,TRAVERSE_MODE, favorability="040", isOldCg=False)) == 0:
                        is_40_ok = True
                if not is_100_ok :
                    if Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID, randomCode,TRAVERSE_MODE, favorability="100", isOldCg=False)) == 0:
                        is_100_ok = True
                if is_40_ok and is_100_ok:
                    print("40 and 100 has find and save to files")
                    break
        elif row['favorability'] != '' and randomCode != '' and not TRAVERSE_MODE:
            if randomCode.__len__() == 4:
                if not Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID, randomCode,TRAVERSE_MODE, row["favorability"], isOldCg=False)):
                    print("finish save " + row['favorability'] + " favorability cg" + charaID)
            elif randomCode.__len__() == 7:
                if not Util.checkErrorCode(GetCG.getCG(defURL, charaID, charaFileID, randomCode,TRAVERSE_MODE, row["favorability"], isOldCg=True)):
                    print("finish save " + row["favorability"] +" favorability cg" + charaID)
        elif row['favorability'] == '0' and randomCode == '0':
            print("the chara no have cg")
