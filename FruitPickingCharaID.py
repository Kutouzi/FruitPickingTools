import CheckData
import GetURL
import Util
import pandas as pd
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor,as_completed

# 此主函数是用于检测漏掉的角色id并更新到缓存csv用的，目前不会用到，请直接执行FruitPickingTools主函数
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

    # table = pd.read_csv("./charaMap/charaData.csv",
    #                     converters={'charaID':str,'charaFileID':str,'favorability':str,'randomCode':str})
    # if 'a' in table:
    #     print("table['a']")

    # with ThreadPoolExecutor(max_workers=100) as pool:
    #     reqs = [pool.submit(Util.ass,it) for it in range(1,6)]
    #     for req in as_completed(reqs):
    #         print(req.result())

    IDString = ""
    beginRange = 225
    endRange = 225
    hiatusTable = CheckData.checkInfo(beginRange,endRange)
    while hiatusTable:
        print(hiatusTable.__len__())
        IDString = GetURL.getURL(GetURL.randomIDSet(f'{hiatusTable.pop():03d}'))
        print(IDString)
        if CheckData.checkHiatusID(IDString,beginRange,endRange):
            Util.insertID(IDString)

    shortURL = ''
    charaID =''
    charaFileID = ''
    favorability = ''
    randomCode =''
    Util.insertRandomCode(charaID,charaFileID,favorability,randomCode)



