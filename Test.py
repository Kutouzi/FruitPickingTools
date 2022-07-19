import CheckData
import GetURL
import Util
import pandas as pd

if __name__ == '__main__':
    # table = pd.read_csv("./charaMap/charaData.csv",
    #                     converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    # for index,row in table.iterrows():
    #     if row["charaID"] == '057' and row["favorability"] == '':
    #         row.at['favorability'] = "040"
    #         row.at['randomCode'] = "AAAA"
    #         print(row)
    # print(CheckData.checkHiatusRandomCode().__len__())

    # strs = 'aaaa_ss'
    # print(strs.split('_')[0])

    table = pd.read_csv("./charaMap/charaData.csv",
                        converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    if 'a' in table:
        print("table['a']")
    # IDString = ""
    # hiatusTable = CheckData.checkInfo()
    # while hiatusTable:
    #     print(hiatusTable.__len__())
    #     IDString = GetURL.getURL(GetURL.randomIDSet(f'{hiatusTable.pop():03d}'))
    #     print(IDString)
    #     if CheckData.checkHiatusID(IDString):
    #         Util.insertID(IDString)




