import os
import pandas as pd

#未完成，请勿使用
if __name__ == "__main__":
    if os.path.exists("./formatoutput"):
        pass
    else:
        try:
            os.mkdir("./formatoutput")
        except:
            print(r"cant create directory './formatoutput'")
            exit(-1)

    tables = pd.read_csv("./charaMap/charaData.csv",
                         converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    oldOutputSet = set()
    for root, dirs, files in os.walk('./output',topdown=False):
        oldOutputSet.add(dirs)
    deep_1 = ''
    for root, dirs, files in os.walk('./output',topdown=False):
        oldOutputSet.add(dirs)
