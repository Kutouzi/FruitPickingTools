import os
import pandas as pd
import TraversCG

# 用于遍历或者下载cg到本地的主函数，TRAVERSE_MODE只供开发者使用，正常使用请设置为False
if __name__ == '__main__':
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
    TRAVERSE_MODE:bool = True
    specifyCharaID = '473'
    specifyCharaFileID = 'E86'
    TraversCG.traversCG(tables,TRAVERSE_MODE,specifyCharaID,specifyCharaFileID)
