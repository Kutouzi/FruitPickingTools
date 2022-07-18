import CheckData

if __name__ == '__main__':
    # CheckData.checkInfo()
    step = 0
    IDString = "240E2I"
    if step == 0:
        if CheckData.checkHiatusID(IDString):
            step = 1
    if step == 1:
        CheckData.insertID(IDString)
