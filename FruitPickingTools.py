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
    varTables = pd.read_csv("./var/var.csv",converters={'var':str,'value':str})
    TRAVERSE_MODE:bool = False
    specifyCharaID:str = ''
    specifyCharaFileID:str = ''
    startRandomCode:str=''
    for index,row in varTables.iterrows():
        if row['var'] == 'TRAVERSE_MODE':
            TRAVERSE_MODE:bool = bool(int(row['value']))
        if row['var'] == 'specifyCharaID':
            specifyCharaID = row['value']
        if row['var'] == 'specifyCharaFileID':
            specifyCharaFileID = row['value']
        if row['var'] == 'startRandomCode':
            startRandomCode=row['value']
            if startRandomCode.__len__() != 4 and not startRandomCode.isalpha():
                print(r"randomCode invalid")
                startRandomCode=''
    TraversCG.traversCG(tables,startRandomCode,TRAVERSE_MODE,specifyCharaID,specifyCharaFileID)
