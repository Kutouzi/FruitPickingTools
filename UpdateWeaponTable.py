import os
from pathlib import Path

import pandas as pd

def traverseOutputFile(path:str):
    aList = []
    for root, dirs, files in os.walk(path,topdown=False):
        aList.append(files)
    return set(aList.pop())

if __name__ == '__main__':
    OutputSet = traverseOutputFile("./game/assets/equip/icon/")
    tablesC = pd.read_csv("./weaponMap/weaponData_C.csv",
                         converters={'identity':str,'weaponID':str,'hashCode':str})
    idSetC=set()
    for index,row in tablesC.iterrows():
        idSetC.add(int(row['weaponID']))

    tablesW = pd.read_csv("./weaponMap/weaponData_W.csv",
                          converters={'identity':str,'weaponID':str,'hashCode':str})
    idSetW=set()

    isExist = False
    for index,row in tablesC.iterrows():
        idSetW.add(int(row['weaponID']))

    while OutputSet:
        fileName = OutputSet.pop()
        if fileName[:1] =='C':
            for _ in idSetC:
                if _ == int(fileName[1:4]):
                    isExist = True
                    break
            if not isExist :
                tablesC.loc[tablesC.__len__()+2] = [fileName[:1],fileName[1:4],fileName[4:6]]
            isExist = False
        if fileName[:1] =='W':
            for _ in idSetW:
                if _ == int(fileName[1:4]):
                    isExist = True
                    break
            if not isExist :
                tablesW.loc[tablesC.__len__()+2] = [fileName[:1],fileName[1:4],fileName[4:6]]
            isExist = False

    resultTableC = tablesC.sort_values(by='weaponID',ascending=True)
    resultTableC.to_csv("./weaponMap/weaponData_C.csv",index=False)

    resultTableW = tablesW.sort_values(by='weaponID',ascending=True)
    resultTableW.to_csv("./weaponMap/weaponData_W.csv",index=False)



