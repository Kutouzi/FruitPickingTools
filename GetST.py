import numpy
from loguru import logger
import Util
import httpx

def getST(defURL:str, charaID:str, charaFileID:str):
    fullStandURL = defURL + charaID + charaFileID + '/full'
    StandURL = defURL + charaID + charaFileID + '/st'
    evoCharaFileID = list(charaFileID)
    evoCharaFileID[0] = 'T'
    evoCharaFileID = ''.join(evoCharaFileID)
    retry_count = 12
    maxArray=numpy.arange(100)
    # 储存高像素立绘
    is403T = False
    is403E = False
    for __ in maxArray:
        if is403T and is403E:
            logger.info(charaID + " all high pixels stand have been saved")
            break
        imageName = charaID + charaFileID + '_' + f'{__:02d}' + ".png"
        evoImageName = charaID + evoCharaFileID + '_' + f'{__:02d}' + ".png"
        isFinishT = False
        isFinishE = False
        for _ in range(retry_count):
            try:
                if isFinishT and isFinishE:
                    break
                if not isFinishT:
                    data = httpx.get(StandURL + "/" + imageName,timeout=5)
                    if data.status_code == 200:
                        logger.info("high pixels stand "+ imageName + " have been found")
                        Util.saveSTResource(data.content,charaID,charaFileID,imageName,isHighPixel=True)
                        isFinishT = True
                    if data.status_code == 403:
                        is403T = True
                if not isFinishE:
                    evoData = httpx.get(StandURL + "/" + evoImageName,timeout=5)
                    if evoData.status_code == 200:
                        logger.info("evolution high pixel stand " + evoImageName +" have been found")
                        Util.saveSTResource(evoData.content,charaID,charaFileID,evoImageName,isHighPixel=True)
                        isFinishE = True
                    if evoData.status_code == 403:
                        is403E = True
            except:
                logger.warning("get image "+charaID + charaFileID +'_'+ f'{__:02d}' +" timeout. retry " + (_+1).__str__() )

    isSavedE = False
    isSavedT = False
    # 储存全立绘
    for _ in range(retry_count):
        if isSavedE and isSavedT:
            logger.info(charaID + " all full stand have been saved")
            break
        try:
            fullImageName = charaID + charaFileID + ".png"
            evoFullImageName = charaID + evoCharaFileID + ".png"
            data = httpx.get(fullStandURL + "/" + fullImageName,timeout=5)
            evoData = httpx.get(fullStandURL + "/" + evoFullImageName,timeout=5)
            if data.status_code == 200:
                logger.info(charaID + " stand have been found")
                Util.saveSTResource(data.content,charaID,charaFileID,fullImageName,isHighPixel=False)
                isSavedT=True
            if evoData.status_code == 200:
                logger.info(charaID + " evolution full have been found")
                Util.saveSTResource(evoData.content,charaID,charaFileID,evoFullImageName,isHighPixel=False)
                isSavedE=True
        except:
            logger.warning(f"get image "+ charaID + charaFileID + "timeout. retry "+(_+1).__str__())
    return 0