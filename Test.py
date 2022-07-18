import CheckData
import GetURL

if __name__ == '__main__':
    step = 3
    IDString = "262E6A"
    # {153, 154, 411, 155, 431, 432, 433, 306, 188, 61, 78, 208,
    # 81, 209, 468, 469, 472, 473, 474, 475, 476, 477, 478, 479, 480, 225, 481,
    # 482, 483, 484, 485, 359, 360, 486, 487, 488, 489, 490, 491, 239, 492, 241,
    # 493, 494, 495, 496, 497, 498, 499}
    while(step == 3):
        if CheckData.checkInfo().__len__() <= 0:
            break
        if step ==3:
            tmpStr = str(CheckData.checkInfo().pop())
            if tmpStr.__len__() == 3:
                IDString = GetURL.getURL(GetURL.randomIDSet(tmpStr))
            else:
                IDString = GetURL.getURL(GetURL.randomIDSet("0" + tmpStr))
            print(IDString)
            step = 0
        if step == 0:
            if CheckData.checkHiatusID(IDString):
                step = 1
        if step == 1:
            CheckData.insertID(IDString)
            step = 4
        if step == 4:
            CheckData.checkInfo()
            step = 3



