from loguru import logger
import Util
import httpx

def getST(defURL:str, charaID:str, charaFileID:str):
    fullStandURL = defURL + charaID + charaFileID + '/full/' + charaID + charaFileID
    StandURL = defURL + charaID + charaFileID + '/st/' + charaID + charaFileID
    evoCharaFileID = list(charaFileID)
    evoCharaFileID[0] = 'T'
    evoCharaFileID = ''.join(evoCharaFileID)
    evoFullStandURL = defURL + charaID + charaFileID + '/full/' + charaID + evoCharaFileID
    evoStandURL = defURL + charaID + charaFileID + '/st/' + charaID + evoCharaFileID
    retry_count = 3
    isSaved00 = False
    isSaved01 = False
    # TODO 此处高冗余，待简化
    # 储存高像素的进化前立绘
    for _ in range(retry_count):
        try:
            imageName00 = charaID + charaFileID + '_00' + ".png"
            imageName01 = charaID + charaFileID + '_01' + ".png"
            data00 = httpx.get(StandURL + "/" + imageName00,timeout=5)
            data01 = httpx.get(StandURL + "/" + imageName01,timeout=5)
            if data00.status_code == 200 and not isSaved00:
                logger.info(charaID + "high pixel stand 1 has find")
                Util.saveSTResource(data00.content,charaID,imageName00,isHighPixel=True)
                isSaved00 = True
            elif data00.status_code == 200 and isSaved00:
                logger.warning(f"image {imageName00} has saved")
            else:
                logger.warning(f"get image {imageName00} timeout")

            if  data01.status_code == 200 and not isSaved01:
                logger.info(charaID + "high pixel stand 2 has find")
                Util.saveSTResource(data01.content,charaID,imageName01,isHighPixel=True)
                isSaved01 = True
            elif data01.status_code == 200 and isSaved01:
                logger.warning(f"image {imageName01} has saved")
            else:
                logger.warning(f"get image {imageName01} timeout")
        except:
            pass
    # 储存普通的进化后立绘
    for _ in range(retry_count):
        try:
            evoFullImageName00 = charaID + evoCharaFileID + '_00' + ".png"
            evoFullImageName01 = charaID + evoCharaFileID + '_01' + ".png"
            data00 = httpx.get(fullStandURL + "/" + evoFullImageName00,timeout=5)
            data01 = httpx.get(fullStandURL + "/" + evoFullImageName01,timeout=5)
            if data00.status_code == 200 and data01.status_code == 200:
                logger.info(charaID + " stand 1 has find")
                Util.saveSTResource(data00.content,charaID,evoFullImageName00,isHighPixel=False)
                isSaved00 = True
            elif data00.status_code == 200 and isSaved00:
                logger.warning(f"image {evoFullImageName00} has saved")
            else:
                logger.warning(f"get image {evoFullImageName00} timeout")

            if  data01.status_code == 200 and not isSaved01:
                logger.info(charaID + "stand 2 has find")
                Util.saveSTResource(data01.content,charaID,evoFullImageName01,isHighPixel=False)
                isSaved00 = True
            elif data01.status_code == 200 and isSaved01:
                logger.warning(f"image {evoFullImageName01} has saved")
            else:
                logger.warning(f"get image {evoFullImageName01} timeout")
        except:
            pass
    # 储存高像素的进化后立绘
    for _ in range(retry_count):
        try:
            evoImageName00 = charaID + evoCharaFileID + '_00' + ".png"
            evoImageName01 = charaID + evoCharaFileID + '_01' + ".png"
            data00 = httpx.get(evoStandURL + "/" + evoImageName00,timeout=5)
            data01 = httpx.get(evoStandURL + "/" + evoImageName01,timeout=5)
            if data00.status_code == 200 and not isSaved00:
                logger.info(charaID + "high pixel stand 1 has find")
                Util.saveSTResource(data00.content,charaID,evoImageName00,isHighPixel=True)
                isSaved00 = True
            elif data00.status_code == 200 and isSaved00:
                logger.warning(f"image {evoImageName00} has saved")
            else:
                logger.warning(f"get image {evoImageName00} timeout")

            if  data01.status_code == 200 and not isSaved01:
                logger.info(charaID + "high pixel stand 2 has find")
                Util.saveSTResource(data01.content,charaID,evoImageName01,isHighPixel=True)
                isSaved01 = True
            elif data01.status_code == 200 and isSaved01:
                logger.warning(f"image {evoImageName01} has saved")
            else:
                logger.warning(f"get image {evoImageName01} timeout")
        except:
            pass
    # 储存普通的进化前立绘
    for _ in range(retry_count):
        try:
            fullImageName00 = charaID + charaFileID + '_00' + ".png"
            fullImageName01 = charaID + charaFileID + '_01' + ".png"
            data00 = httpx.get(evoFullStandURL + "/" + fullImageName00,timeout=5)
            data01 = httpx.get(evoFullStandURL + "/" + fullImageName01,timeout=5)
            if data00.status_code == 200 and data01.status_code == 200:
                logger.info(charaID + " stand 1 has find")
                Util.saveSTResource(data00.content,charaID,fullImageName00,isHighPixel=False)
                isSaved00 = True
            elif data00.status_code == 200 and isSaved00:
                logger.warning(f"image {fullImageName00} has saved")
            else:
                logger.warning(f"get image {fullImageName00} timeout")

            if  data01.status_code == 200 and not isSaved01:
                logger.info(charaID + "stand 2 has find")
                Util.saveSTResource(data01.content,charaID,fullImageName01,isHighPixel=False)
                isSaved00 = True
            elif data01.status_code == 200 and isSaved01:
                logger.warning(f"image {fullImageName01} has saved")
            else:
                logger.warning(f"get image {fullImageName01} timeout")
        except:
            pass
    return 0