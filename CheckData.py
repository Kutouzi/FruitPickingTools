import pandas as pd

def checkHiatusID(IDString:str):
    if IDString.__len__() == 6 and IDString[3:4] == 'E':
        id = IDString[:3]
        fileID = IDString[3:]
        table = pd.read_csv("./charaMap/charaData.csv",
                            converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
        numList:set = set(range(1,500))
        hiatusTable:set = set()
        IDTable:set = set()
        for index,row in table.iterrows():
            a = int(row['charaID'])
            IDTable.add(a)
        hiatusTable =  set(numList) - set(IDTable)
        find = int(id)
        for id in hiatusTable:
            if id == find:
                print("find")
                return True
    print("error data or exiet data")
    return False

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
            resultTable = table.sort_values(by='charaID',ascending=True)
            resultTable.to_csv("./charaMap/charaData.csv",index=False)
            print("update table")

def checkInfo():
    table = pd.read_csv("./charaMap/charaData.csv",
                        converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    numList:set = set(range(1,500))
    hiatusTable:set = set()
    IDTable:set = set()
    for index,row in table.iterrows():
        a = int(row['charaID'])
        IDTable.add(a)
    hiatusTable =  set(numList) - set(IDTable)
    #print(hiatusTable)
    #print("have " + hiatusTable.__len__().__str__() + "cow no data")
    return hiatusTable