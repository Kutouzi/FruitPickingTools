import Util
import httpx
import pandas as pd

from io import BytesIO
from loguru import logger

def getCG(defURL:str, charaID:str, charaFileID:str, randomCode:str, TRAVERSE_MODE:bool, retryCount:int, silentMode:bool, favorability:str, isOldCg:bool):
    #logger.info("now is " +charaID + " " + randomCode + " favorability:" + favorability)
    if isOldCg:
        dataURL = defURL + "/" + charaID.__str__() + charaFileID + "/" + favorability + randomCode + "_R"
    else:
        dataURL = defURL + "/" + charaID.__str__() + charaFileID + "/" + favorability + randomCode + charaID.__str__() + "_R"
    if silentMode == True:
        if len(set(list(randomCode))) == 1:
            logger.warning(f"now, traverse progress is { randomCode }/ZZZZ at favorability {favorability}")
    for _ in range(retryCount):
        try:
            if silentMode == False:
                logger.info(f"try to test {charaID} at favorability {favorability}. randomCode:{randomCode}")
            data = httpx.get(dataURL + "/data.txt",timeout=5)
            if data.status_code == 200:
                logger.info("charaID: " + charaID + ", favorability:" + favorability +", data has been found, the randomCode is " + randomCode)
                if TRAVERSE_MODE:
                    # 更新csv缓存文件
                    Util.insertRandomCode(charaID, charaFileID, favorability, randomCode)
                # 保存cg文件
                table=pd.read_csv(BytesIO(data.content)).fillna('')
                imageCollection = set(it for it in table['background'] if it.startswith('HCG'))
                backgroundCollection = set(it for it in table['background'] if not it.startswith('HCG'))
                if imageCollection.__len__() > 0:
                    for it in imageCollection:
                        imageName = it + ".jpg"
                        imageURL = dataURL + "/images/" + imageName
                        for count in range(retryCount):
                            try:
                                image = httpx.get(imageURL).content
                                Util.saveResource(image,charaID,charaFileID,randomCode,favorability,imageName,isOldCg,isMovie=False)
                                break
                            except:
                                pass
                        else:
                            logger.warning(f"get image {imageName} timeout")
                    if backgroundCollection.__len__() > 0:
                        for it in backgroundCollection:
                            backgroundName = it + ".jpg"
                            backgroundURL =  'http://fruful.jp/img/game/asset/background/event/' + backgroundName
                            for count in range(retryCount):
                                try:
                                    background = httpx.get(backgroundURL).content
                                    Util.saveBGResource(background,backgroundName)
                                    break
                                except:
                                    pass
                            else:
                                logger.warning(f"get image {backgroundName} timeout")
                    return 0
                else:
                    movieCollection = set(it.split('_')[0] for it in table['movie'] if it)
                    if movieCollection.__len__() > 0:
                        for it in movieCollection:
                            movieName = it + ".mp4"
                            movieURL = dataURL + "/movie/" + movieName
                            for count in range(retryCount):
                                try:
                                    movie = httpx.get(movieURL).content
                                    Util.saveResource(movie,charaID,charaFileID,randomCode,favorability,movieName,isOldCg,isMovie=True)
                                    break
                                except:
                                    logger.warning(f"get movie {movieName} timeout")
                        return 0
                    else:
                        return 2
            if data.status_code == 403:
                break
        except:
            logger.warning(f"favorability {favorability} and randomCode:{randomCode}, request timeout, {_ + 1} retry")
    return 3
