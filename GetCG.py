import Util
import httpx
import pandas as pd

from io import BytesIO

def getCG(defURL:str, charaID:str, charaFileID:str, randomCode:str, favorability:str, isOldCg:bool):
    #人物代码+E？？/好感值+？？？？+人物代码
    #例如334E9Z/100TYVH334_R
    #又如334E9Z/040KEBL334_R
    #前半段可直接打开面板就能看，结构为数字ID+E+两个字符（0-9或A-Z）
    #后半段结构为好感值（一般有两个分别为40好感时和100好感时hs）+四个字符（A-Z）+人物代码+_R
    if isOldCg:
        dataURL = defURL + "/" + charaID.__str__() + charaFileID + "/" + favorability + randomCode + "_R"
    else:
        dataURL = defURL + "/" + charaID.__str__() + charaFileID + "/" + favorability + randomCode + charaID.__str__() + "_R"

    try:
        data = httpx.get(dataURL + "/data.txt",timeout=5)
        if data.status_code == 200:
            print("find " + randomCode)
            # 更新csv缓存文件
            Util.insertRandomCode(charaID, charaFileID, favorability, randomCode)
            # 保存cg文件
            table=pd.read_csv(BytesIO(data.content))
            imageCollection = set(it for it in table['background'].to_list() if it.startswith('HCG'))
            if imageCollection.__len__() > 0:
                for it in imageCollection:
                    imageName = it + ".jpg"
                    imageURL = dataURL + "/images/" + imageName
                    image = httpx.get(imageURL).content
                    if Util.saveResource(image,charaID,imageName,favorability) == 0:
                        return 0
                    else:
                        return 3
            else:
                movieCollection = set(it for it in table['movie'].to_list())
                if movieCollection.__len__() > 0:
                    movieName = movieCollection.pop() + ".mp4"
                    movieURL = dataURL + "/movie/" + movieName
                    movie = httpx.get(movieURL).content
                    if Util.saveResource(movie,charaID,movieName,favorability) == 0:
                        return 0
                    else:
                        return 3
                else:
                    return 2
    except:
        print(randomCode + " time out 1")
        try:
            data = httpx.get(dataURL + "/data.txt",timeout=5)
            if data.status_code == 200:
                table=pd.read_csv(BytesIO(data.content))
                print(randomCode)
                imageCollection = set(it for it in table['background'].to_list() if it.startswith('HCG'))
                if imageCollection.__len__() > 0:
                    for it in imageCollection:
                        imageName = it + ".jpg"
                        imageURL = dataURL + "/images/" + imageName
                        image = httpx.get(imageURL).content
                        if Util.saveResource(image,charaID,imageName,favorability) == 0:
                            return 0
                        else:
                            return 3
                else:
                    movieCollection = set(it for it in table['movie'].to_list())
                    if movieCollection.__len__() > 0:
                        movieName = movieCollection.pop() + ".mp4"
                        movieURL = dataURL + "/movie/" + movieName
                        movie = httpx.get(movieURL).content
                        if Util.saveResource(movie,charaID,movieName,favorability) == 0:
                            return 0
                        else:
                            return 3
                    else:
                        return 2
        except:
            print(randomCode + " time out 2")
            try:
                data = httpx.get(dataURL + "/data.txt",timeout=5)
                if data.status_code == 200:
                    table=pd.read_csv(BytesIO(data.content))
                    print(randomCode)
                    imageCollection = set(it for it in table['background'].to_list() if it.startswith('HCG'))
                    if imageCollection.__len__() > 0:
                        for it in imageCollection:
                            imageName = it + ".jpg"
                            imageURL = dataURL + "/images/" + imageName
                            image = httpx.get(imageURL).content
                            if Util.saveResource(image,charaID,imageName,favorability) == 0:
                                return 0
                            else:
                                return 3
                    else:
                        movieCollection = set(it for it in table['movie'].to_list())
                        if movieCollection.__len__() > 0:
                            movieName = movieCollection.pop() + ".mp4"
                            movieURL = dataURL + "/movie/" + movieName
                            movie = httpx.get(movieURL).content
                            if Util.saveResource(movie,charaID,movieName,favorability) == 0:
                                return 0
                            else:
                                return 3
                        else:
                            return 2
            except:
                print(randomCode + " time out 3")
                return 1

