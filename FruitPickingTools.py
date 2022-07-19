import os
import pandas as pd
import GetCG as cg
import Util

if __name__ == '__main__':
    defURL = r"http://fruful.jp/img/game/chara/event"
    is_40_ok:bool = False
    is_100_ok:bool = False
    checkCode = 1
    #必定已知参数之后会以csv格式存在charaMap文件夹下
    charaID:int = 334
    charaFileID:str = "E9Z"

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
        resultString = row['randomCode']
        if row['favorability'] == '' or resultString == '':
            charaID = row['charaID']
            charaFileID = row['charaFileID']
            if resultString == '':
                for resultString in Util.yield_str():
                    if not is_40_ok :
                        if Util.checkErrorCode(cg.getCG(defURL,charaID,charaFileID,resultString,favorability="040") == 0):
                            is_40_ok = True
                    if not is_100_ok :
                        if Util.checkErrorCode(cg.getCG(defURL, charaID, charaFileID,resultString, favorability="100") == 0):
                            is_100_ok = True
                    if is_40_ok and is_100_ok:
                        break
        else:
            Util.checkErrorCode(cg.getCG(defURL,charaID,charaFileID,resultString,favorability="040") == 0)
            Util.checkErrorCode(cg.getCG(defURL, charaID, charaFileID,resultString, favorability="100") == 0)

