import pandas as pd

def checkHiatusID(IDString:str):
    if IDString.__len__() == 6 and IDString[3:4] == 'E':
        id = IDString[:3]
        find = int(id)
        h = checkInfo()
        for id in h:
            if id == find:
                print("find " + IDString)
                return True
        print("exiet data: " + IDString)
    else:
        print("error data: " + IDString)
    return False

def checkInfo():
    table = pd.read_csv("./charaMap/charaData.csv",
                        converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    numList:set = set(range(1,471+1))
    hiatusTable:set = set()
    IDTable:set = set()
    for index,row in table.iterrows():
        a = int(row['charaID'])
        IDTable.add(a)
    hiatusTable =  set(numList) - set(IDTable)
    #print(hiatusTable)
    #print("have " + hiatusTable.__len__().__str__() + "cow no data")
    return hiatusTable

def checkHiatusRandomCode():
    table = pd.read_csv("./charaMap/charaData.csv",
                        converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    hiatusRandomCodeSet:set = set()
    for index,row in table.iterrows():
        if row['randomCode'] == '':
            hiatusRandomCodeSet.add(row['charaID'])
    return hiatusRandomCodeSet