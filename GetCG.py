import Util
import httpx
import pandas as pd

from io import BytesIO
from loguru import logger

logger.add('./logs/getlog_{time}.log', format="{name} {level} {message}", level="DEBUG", rotation='5 MB', encoding='utf-8')

def getCG(defURL:str, charaID:str, charaFileID:str, randomCode:str,TRAVERSE_MODE:bool, favorability:str, isOldCg:bool):
    #人物代码+E？？/好感值+？？？？+人物代码
    #例如334E9Z/100TYVH334_R
    #又如334E9Z/040KEBL334_R
    #前半段可直接打开面板就能看，结构为数字ID+E+两个字符（0-9或A-Z）
    #后半段结构为好感值（一般有两个分别为40好感时和100好感时hs）+四个字符（A-Z）+人物代码+_R
    #logger.info("now is " +charaID + " " + randomCode + " favorability:" + favorability)
    if isOldCg:
        dataURL = defURL + "/" + charaID.__str__() + charaFileID + "/" + favorability + randomCode + "_R"
    else:
        dataURL = defURL + "/" + charaID.__str__() + charaFileID + "/" + favorability + randomCode + charaID.__str__() + "_R"

    retry_count = 3
    for _ in range(retry_count):
        try:
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
                        for count in range(retry_count):
                            try:
                                image = httpx.get(imageURL).content
                                Util.saveResource(image,charaID,imageName,favorability)
                                break
                            except:
                                pass
                        else:
                            logger.warning(f"获取图像{imageName}请求超时")
                    return 0
                else:
                    movieCollection = set(it.split('_')[0] for it in table['movie'] if it)
                    if movieCollection.__len__() > 0:
                        for it in movieCollection:
                            movieName = it + ".mp4"
                            movieURL = dataURL + "/movie/" + movieName
                            for count in range(retry_count):
                                try:
                                    movie = httpx.get(movieURL).content
                                    Util.saveResource(movie,charaID,movieName,favorability)
                                    break
                                except:
                                    logger.warning(f"获取视频{movieName}请求超时")
                        return 0
                    else:
                        return 2
        except:
            pass
    return 3
