import CheckData

if __name__ == '__main__':
    step = 0
    IDString = "450EL7"
    if step == 0:
        if CheckData.checkHiatusID(IDString):
            step = 1
    if step == 1:
        CheckData.insertID(IDString)