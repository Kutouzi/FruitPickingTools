import pandas as pd

def checkHiatusID():
    table = pd.read_csv("./charaMap/charaData.csv",
                        converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    # charaIDTable = table.loc[['charaID']]
    numList:set = set(range(1,500))
    hiatusTable:set = set()
    IDTable:set = set()
    for index,row in table.iterrows():
        a = int(row['charaID'])
        IDTable.add(a)
    hiatusTable =  set(numList) - set(IDTable)
    find =467
    for id in hiatusTable:
        if id == find:
            print("exiet")