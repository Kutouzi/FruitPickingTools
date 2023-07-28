import os
from pathlib import Path

import pandas as pd

def checkErrorCode(errorCode:int):
    if errorCode == 0:
        return 0
    elif errorCode == 1:
        print("network error, please check the local network")
        return 1
    elif errorCode == 2:
        print("resource error, the resource is empty on the server")
        return 2
    elif errorCode == 3:
        #print("error random code.")
        return 3

def yield_str(argList:list):
    if argList.__len__() == 0:
        argList=[65,65,65,65]
    isOnce=True
    for chs in map(chr, range(argList[0], 90+1)):
        str=''
        str+=chs
        if isOnce:
            isOnce=False
        else:
            argList[1]=65
            argList[2]=65
            argList[3]=65
        for chs in map(chr, range(argList[1], 90+1)):
            str+=chs
            for chs in map(chr, range(argList[2], 90+1)):
                str+=chs
                for chs in map(chr, range(argList[3], 90+1)):
                    str+=chs
                    yield str
                    str=str[0:3]
                str=str[0:2]
            str=str[0:1]
def insertRandomCode(charaID:str,charaFileID:str,favorability:str,randomCode:str):
    if randomCode.__len__() == 4:
        table = pd.read_csv("./charaMap/charaData.csv",
                            converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
        for index,row in table.iterrows():
            if  row['charaID'] == charaID and row['favorability'] == '':
                row.at['favorability'] = favorability
                row.at['randomCode'] = randomCode
                updateTable(table)
                break
            elif row['charaID'] == charaID and row['favorability'] == favorability:
                row.at['randomCode'] = randomCode
                updateTable(table)
                break
            elif row['charaID'] == charaID and row['favorability'] != '':
                table.loc[table.__len__()+2] = [charaID,charaFileID,favorability,randomCode]
                updateTable(table)
                break

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
    print("charaData.csv table updated")

def saveBGResource(resource,resourceName):
    path = Path('./outputbg')
    try:
        path.mkdir(parents=True,exist_ok=True)
    except:
        print("error creating directory: " + path.__str__())
    try:
        (path / (resourceName)).write_bytes(resource)
    except:
        print("error writing to file: " + resourceName)
    return 0
#image,charaID,charaFileID,randomCode,favorability,imageName
def saveResource(resource,charaID:str,charaFileID:str,randomCode:str,favorability:str,resourceName:str,isOldCg,isMovie):
    if isMovie:
        if isOldCg:
            path = Path("./output/") / (charaID+charaFileID) / (favorability+randomCode+'_R') / Path("./movie")
        else:
            path = Path("./output/") / (charaID+charaFileID) / (favorability+randomCode+charaID+'_R') / Path("./movie")
    else:
        if isOldCg:
            path = Path("./output/") / (charaID+charaFileID) / (favorability+randomCode+'_R') / Path("./images")
        else:
            path = Path("./output/") / (charaID+charaFileID) / (favorability+randomCode+charaID+'_R') / Path("./images")
    try:
        path.mkdir(parents=True,exist_ok=True)
    except:
        print("error creating directory: " + path.__str__() + favorability)
    try:
        (path / (resourceName)).write_bytes(resource)
    except:
        print("error writing to file: " + charaID + " " + resourceName)
    return 0

def saveSTResource(resource,charaID:str,CharaFileID:str,resourceName:str,isHighPixel:bool):
    if isHighPixel:
        path = Path("./outputst/") / Path(charaID + CharaFileID) / Path("st")
    else:
        path = Path("./outputst/") / Path(charaID + CharaFileID) / Path('full')
    try:
        path.mkdir(parents=True,exist_ok=True)
    except:
        print("error creating directory: " + path.__str__())
    try:
        (path / (resourceName)).write_bytes(resource)
    except:
        print("error writing to file: " + charaID + " " + resourceName)
    return 0

def traverseOutputFile(path:str):
    aList = []
    for root, dirs, files in os.walk(path,topdown=False):
        aList.append(dirs)
    return set(aList.pop())
