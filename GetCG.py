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
            logger.warning(f"now, traverse progress is { randomCode }/ZZZZ ")
    for _ in range(retryCount):
        try:
            if silentMode == False:
                logger.info(f"try to test {charaID} at favorability {favorability}. randomCode:{randomCode}")
            data = httpx.get(dataURL + "/data.txt",timeout=5)
            if data.status_code == 200:
                logger.info(charaID + " favorability:" + favorability +" has find " + randomCode)
                if TRAVERSE_MODE:
                    # 更新csv缓存文件
                    Util.insertRandomCode(charaID, charaFileID, favorability, randomCode)
                # 保存cg文件
                table=pd.read_csv(BytesIO(data.content)).fillna('')
                imageCollection = set(it for it in table['background'] if it.startswith('HCG'))
                if imageCollection.__len__() > 0:
                    for it in imageCollection:
                        imageName = it + ".jpg"
                        imageURL = dataURL + "/images/" + imageName
                        for count in range(retryCount):
                            try:
                                image = httpx.get(imageURL).content
                                Util.saveResource(image,charaID,imageName,favorability)
                                break
                            except:
                                pass
                        else:
                            logger.warning(f"get image {imageName} timeout")
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
                                    Util.saveResource(movie,charaID,movieName,favorability)
                                    break
                                except:
                                    logger.warning(f"get movie {movieName} timeout")
                        return 0
                    else:
                        return 2
            if data.status_code == 403:
                break
        except:
            logger.warning(f"randomCode:{randomCode} request timeout, retry {_ + 1}")
    return 3
