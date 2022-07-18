import CheckData
import GetURL

if __name__ == '__main__':
    step = 3
    IDString = "262E6A"
    # {153, 154, 411, 155, 431, 432, 433, 306, 188, 61, 78, 208,
    # 81, 209, 468, 469, 472, 473, 474, 475, 476, 477, 478, 479, 480, 225, 481,
    # 482, 483, 484, 485, 359, 360, 486, 487, 488, 489, 490, 491, 239, 492, 241,
    # 493, 494, 495, 496, 497, 498, 499}
    hiatusTable = CheckData.checkInfo()
    while hiatusTable:
        IDString = GetURL.getURL(GetURL.randomIDSet(f'{hiatusTable.pop():03d}'))
        print(IDString)
        if CheckData.checkHiatusID(IDString):
            break
        CheckData.insertID(IDString)
        print(hiatusTable.__len__())



