import pandas as pd

if __name__ == "__main__":
    charaData = pd.read_csv("./charaMap/charaData.csv",
                                     converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    frufulTable = pd.read_csv('./charaMap/fruful.csv',converters={'ID':str,'RARE':str,'NAME':str,'Rate40':str,
                                                             'Rate40FileName1':str,'Rate40FileName2':str,
                                                             'Rate100':str,'Rate100FileName1':str,
                                                             'Rate100FileName2':str,'Rate100FileName3':str,
                                                             'Rate100FileName4':str})
    charaNameHashTable = pd.read_csv("./charaMap/charaNameHash.csv",
                                     converters={'charaID':str,'charaFileID':str,'charaName':str,'charaRare':str})
    charaSet = set()
    hashSet = set()

    for index,row in charaData.iterrows():
        charaSet.add(row['charaID']+row['charaFileID'])
    del charaData

    for index,row in charaNameHashTable.iterrows():
        hashSet.add(row['charaID']+row['charaFileID'])
    complementarySet = set(charaSet) - set(hashSet)
    while complementarySet:
        chara = complementarySet.pop()
        charaNameHashTable.loc[charaNameHashTable.__len__()+2] = [chara[:3],chara[3:],'','']
    if not complementarySet :
        print('No data needs to be hashed')
        exit()

    resultTable = charaNameHashTable.sort_values(by='charaID',ascending=True)

    for indexf,rowf in frufulTable.iterrows():
        for index,row in resultTable.iterrows():
            if row['charaID'] == rowf['ID'][:3] and row['charaFileID'] == rowf['ID'][3:]:
                if row['charaName'] == '' and  row['charaRare'] == '':
                    row.at['charaName'] = rowf['NAME']
                    if rowf['RARE'] == '':
                        row.at['charaRare'] = ''
                    else:
                        row.at['charaRare'] = int(rowf['RARE'][1:2])

    resultTable.to_csv("./charaMap/charaNameHash.csv",index=False)
    print('table complete')