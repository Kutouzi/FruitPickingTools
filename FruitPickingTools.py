import os

import GetCG as cg
import Util as ut

if __name__ == '__main__':
    defURL = r"http://fruful.jp/img/game/chara/event"

    #必定已知参数之后会以csv格式存在charaMap文件夹下
    charaID:int = 334
    charaFileID:str = "E9Z"
    is_40_ok:bool = False
    is_100_ok:bool = False
    resultString:str = ""

    checkCode = 1
    if os.path.exists("./output"):
        pass
    else:
        try:
            os.mkdir("./output")
        except:
            print(r"cant create directory './output'")
            exit(-1)
    if resultString == "":
        for resultString in ut.yield_str():
            if not is_40_ok :
                if ut.checkErrorCode(cg.getCG(defURL,charaID,charaFileID,resultString,favorability="040") == 0):
                    is_40_ok = True
            if not is_100_ok :
                if ut.checkErrorCode(cg.getCG(defURL, charaID, charaFileID,resultString, favorability="100") == 0):
                    is_100_ok = True
            if is_40_ok and is_100_ok:
                break
    else:
        ut.checkErrorCode(cg.getCG(defURL,charaID,charaFileID,resultString,favorability="040") == 0)
        ut.checkErrorCode(cg.getCG(defURL, charaID, charaFileID,resultString, favorability="100") == 0)

