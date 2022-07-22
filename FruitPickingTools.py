import os
import pandas as pd
import TraversCG


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
    TraversCG.traversCG(tables)
