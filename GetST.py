from loguru import logger
import Util
import httpx

def getST(defURL:str, charaID:str, charaFileID:str):
    fullStandURL = defURL + charaID + charaFileID + '/full'
    StandURL = defURL + charaID + charaFileID + '/st'
    evoCharaFileID = list(charaFileID)
    evoCharaFileID[0] = 'T'
    evoCharaFileID = ''.join(evoCharaFileID)
    retry_count = 3
    isSaved00 = False
    isSaved01 = False
    # TODO 此处高冗余，待简化
    # 储存高像素的进化前立绘
    for _ in range(retry_count):
        if isSaved00 and isSaved01:
            logger.info(charaID + " all normal high pixels stand have been saved")
            break
        try:
            imageName00 = charaID + charaFileID + '_00' + ".png"
            imageName01 = charaID + charaFileID + '_01' + ".png"
            data00 = httpx.get(StandURL + "/" + imageName00,timeout=5)
            data01 = httpx.get(StandURL + "/" + imageName01,timeout=5)
            if data00.status_code == 200 and not isSaved00:
                logger.info(charaID + " high pixels stand 1 have been found")
                Util.saveSTResource(data00.content,charaID,imageName00,isHighPixel=True)
                isSaved00 = True
            elif data00.status_code == 200 and isSaved00:
                logger.warning(f"image {imageName00} have been saved")
            else:
                logger.warning(f"get image {imageName00} timeout")

            if  data01.status_code == 200 and not isSaved01:
                logger.info(charaID + " high pixels stand 2 have been found")
                Util.saveSTResource(data01.content,charaID,imageName01,isHighPixel=True)
                isSaved01 = True
            elif data01.status_code == 200 and isSaved01:
                logger.warning(f"image {imageName01} have been saved")
            else:
                logger.warning(f"get image {imageName01} timeout")
        except:
            pass
    isSaved00 = False
    isSaved01 = False
    # 储存普通的进化后立绘
    for _ in range(retry_count):
        if isSaved00:
            logger.info(charaID + " all evolution low pixels stand have been saved")
            break
        try:
            evoFullImageName00 = charaID + evoCharaFileID + ".png"
            data00 = httpx.get(fullStandURL + "/" + evoFullImageName00,timeout=5)
            if data00.status_code == 200:
                logger.info(charaID + " evolution low pixels have been found")
                Util.saveSTResource(data00.content,charaID,evoFullImageName00,isHighPixel=False)
                isSaved00 = True
            elif data00.status_code == 200 and isSaved00:
                logger.warning(f"image {evoFullImageName00} have been saved")
            else:
                logger.warning(f"get image {evoFullImageName00} timeout")
        except:
            pass
    isSaved00 = False
    isSaved01 = False
    # 储存高像素的进化后立绘
    for _ in range(retry_count):
        if isSaved00 and isSaved01:
            logger.info(charaID + " all evolution high pixels stand have been saved")
            break
        try:
            evoImageName00 = charaID + evoCharaFileID + '_00' + ".png"
            evoImageName01 = charaID + evoCharaFileID + '_01' + ".png"
            data00 = httpx.get(StandURL + "/" + evoImageName00,timeout=5)
            data01 = httpx.get(StandURL + "/" + evoImageName01,timeout=5)
            if data00.status_code == 200 and not isSaved00:
                logger.info(charaID + " evolution high pixel stand 1 have been found")
                Util.saveSTResource(data00.content,charaID,evoImageName00,isHighPixel=True)
                isSaved00 = True
            elif data00.status_code == 200 and isSaved00:
                logger.warning(f"image {evoImageName00} have been saved")
            else:
                logger.warning(f"get image {evoImageName00} timeout")

            if  data01.status_code == 200 and not isSaved01:
                logger.info(charaID + " evolution high pixel stand 2 have been found")
                Util.saveSTResource(data01.content,charaID,evoImageName01,isHighPixel=True)
                isSaved01 = True
            elif data01.status_code == 200 and isSaved01:
                logger.warning(f"image {evoImageName01} have been saved")
            else:
                logger.warning(f"get image {evoImageName01} timeout")
        except:
            pass
    isSaved00 = False
    isSaved01 = False
    # 储存普通的进化前立绘
    for _ in range(retry_count):
        if isSaved00:
            logger.info(charaID + " all normal low pixels stand have been saved")
            break
        try:
            fullImageName00 = charaID + charaFileID + ".png"
            data00 = httpx.get(fullStandURL + "/" + fullImageName00,timeout=5)
            if data00.status_code == 200:
                logger.info(charaID + " stand have been found")
                Util.saveSTResource(data00.content,charaID,fullImageName00,isHighPixel=False)
                isSaved00 = True
            elif data00.status_code == 200 and isSaved00:
                logger.warning(f"image {fullImageName00} have been saved")
            else:
                logger.warning(f"get image {fullImageName00} timeout")
        except:
            pass
    return 0