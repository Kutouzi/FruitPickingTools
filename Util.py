import os
from pathlib import Path

import pandas as pd
from itertools import product

def checkErrorCode(errorCode:int):
    if errorCode == 0:
        return 0
    elif errorCode == 1:
        print("error network.cant get cg.")
    elif errorCode == 2:
        print("error resource.resource is null in server.")
    elif errorCode == 3:
        print("error random code.")

def yield_str(chr_start=65,chr_end=90):
    for chs in product(map(chr, range(chr_start, chr_end+1)),repeat=4):
        yield ''.join(chs)

def insertRandomCode(charaID:str,charaFileID:str,favorability:str,randomCode:str):
    if randomCode.__len__() == 4:
        table = pd.read_csv("./charaMap/charaData.csv",
                            converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
        for index,row in table.iterrows():
            if  row['charaID'] == charaID and row['favorability'] == '':
                row.at['favorability'] = favorability
                row.at['randomCode'] = randomCode
                updateTable(table)
            elif row['charaID'] == charaID and row['favorability'] == favorability:
                row.at['randomCode'] = randomCode
            elif row['charaID'] == charaID and row['favorability'] != '':
                table.loc[table.__len__()+2] = [charaID,charaFileID,favorability,randomCode]
                updateTable(table)

def insertID(IDString:str):
    if IDString.__len__() == 6:
        id = IDString[:3]
        fileID = IDString[3:]
        table = pd.read_csv("./charaMap/charaData.csv",
                            converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
        IDTable:set = set()
        for index,row in table.iterrows():
            a = int(row['charaID'])
            IDTable.add(a)
        flag = True
        for i in IDTable:
            if i == int(id):
                flag = False
                break
        if flag == True:
            table.loc[table.__len__()+2] = [id,fileID,'','']
            updateTable(table)


def updateTable(table):
    resultTable = table.sort_values(by='charaID',ascending=True)
    resultTable.to_csv("./charaMap/charaData.csv",index=False)
    print("update table")

def saveResource(resource,charaID:str,resourceName:str,favorability:str):
    path = Path("./output/") / charaID / favorability
    try:
        path.mkdir(parents=True,exist_ok=True)
    except:
        print("create dir error " + path.__str__() + favorability)
    try:
        (path / (resourceName)).write_bytes(resource)
    except:
        print("write file error " + charaID + " " + resourceName)
    return 0

def traverseOutputFile(path:str):
    aList = []
    for root, dirs, files in os.walk(path,topdown=False):
        aList.append(dirs)
    return set(aList.pop())
