import os
import pandas as pd
import TraversCG
from loguru import logger

logger.add('./logs/FruitPickingToolsLog_{time}.log', format="{name} {level} {message}", level="DEBUG", rotation='5 MB', encoding='utf-8')

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
    silentMode:bool = False
    specifyCharaID:str = ''
    specifyCharaFileID:str = ''
    startRandomCode:str=''
    specifyFavorability:str=''
    retryCount:int=6
    for index,row in varTables.iterrows():
        if row['var'] == 'TRAVERSE_MODE':
            TRAVERSE_MODE:bool = bool(int(row['value']))
        if row['var'] == 'specifyCharaID':
            specifyCharaID = row['value']
        if row['var'] == 'specifyCharaFileID':
            specifyCharaFileID = row['value']
        if row['var'] == 'specifyFavorability':
            specifyFavorability = row['value']
            if specifyFavorability != '100' and specifyFavorability != '040' and specifyFavorability != '':
                print(r"specifyFavorability value is wrong, it should be 040, 100 or blank'")
                exit(-1)
        if row["var"] == 'retryCount':
            if row['value'] != '':
                retryCount = int(row['value'])
                if retryCount <= 0 :
                    print(r"retryCount value is wrong'")
                    exit(-1)
        if row['var'] == 'startRandomCode':
            startRandomCode=row['value']
            if startRandomCode.__len__() != 4 and not startRandomCode.isalpha():
                print(r"randomCode invalid")
                startRandomCode=''
        if row['var'] == 'silentMode':
            silentMode = bool(int(row['value']))
    TraversCG.traversCG(tables,startRandomCode,TRAVERSE_MODE,specifyCharaID,specifyCharaFileID,specifyFavorability,retryCount,silentMode)
