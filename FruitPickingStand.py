import os
import pandas as pd

import GetST
import Util
from loguru import logger

if __name__ == '__main__':
    if os.path.exists("./outputst"):
        pass
    else:
        try:
            os.mkdir("./outputst")
        except:
            print(r"cant create directory './outputst'")
            exit(-1)

    tables = pd.read_csv("./charaMap/charaData.csv",
                         converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    defURL = r'http://fruful.jp/img/game/chara/graphic/'
    OutputSet = Util.traverseOutputFile("./outputst")
    for index,row in tables.iterrows():
        charaID = row['charaID']
        charaFileID = row['charaFileID']
        if charaID in OutputSet:
            logger.warning(charaID + r" data has exist in ./outputst")
            continue
        if not GetST.getST(defURL, charaID, charaFileID):
            logger.info("finish save " + charaID +" stand")
