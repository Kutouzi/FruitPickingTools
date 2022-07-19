import CheckData
import GetURL

if __name__ == '__main__':
    step = 3
    IDString = "262E6A"
    hiatusTable = CheckData.checkInfo()
    while hiatusTable:
        print(hiatusTable.__len__())
        IDString = GetURL.getURL(GetURL.randomIDSet(f'{hiatusTable.pop():03d}'))
        print(IDString)
        if CheckData.checkHiatusID(IDString):
            CheckData.insertID(IDString)




