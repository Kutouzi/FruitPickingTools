## FruitPickingTools
一个可爬取ふるーつふるきゅーと资源的工具
ふるーつふるきゅーと于2023年8月31日停止运营，停止后此工具将被弃用
此项目已停更，请移步至新项目“FruitsSceneViewer”

>A tool for obtaining fruitsfulcute resource
>ふるーつふるきゅーと will stop operating on August 31, 2023, and this tool will be deprecated after the stop
>This project has been deprecated, please check the new project "FruitsSceneViewer"

目前有的功能：
1. 获取角色HScene（图片与视频）储存于“./output”
2. 获取背景图片储存于“./outputbg”
3. 获取泥石流角色图片储存于“./outputbo”
4. 获取战斗立绘和技能立绘储存于“./outputbt”
5. 获取角色事件剧本（仅40和100好感度）储存于“./outpute”
6. 获取角色水果标志物图标储存于“./outputfic”
7. 获取角色头像储存于“./outputic”
8. 获取角色语音储存于“./outputnv”
9. 获取角色事件语音储存于“./outputv”
10. 获取角色Spine资源储存于“./outputsp”
11. 获取角色立绘和全立绘储存于“./outputst”
12. 获取武器图标储存于“./outputwp”
13. 获取武器图储存于“./outputwpf”
14. 猜测未知角色charaID和charaFile
15. 猜测角色Hscene特殊码，需要调整配置文件“./var/var.csv”来开启

>features:
>1. Obtain character HScene (picture and video) and save in './output'
>2. Obtain background image and save it in "./outputbg"
>3. Obtain mudslide character pictures and save it in "./outputbo"
>4. Obtain combat stand and skill stand are save in "./outputbt"
>5. Obtain character event scripts (only 40 and 100 favorability) save in "./outpute"
>6. Obtain character fruit marker icons save in "./outputfic"
>7. Obtain character avatars and save in "./outputtic"
>8. Obtain the voice of the character and save it in "./outputnv"
>9. Obtain the voice of the character event and save it in "./outputv"
>10. Obtain character Spine resources and save in "./outputsp"
>11. Obtain character stand and full stand and save in "./outputst"
>12. Obtain weapon icons save in "./outputwp"
>13. Obtain the weapon map save in "./outputwpf"
>14. Guess the CharacterID of an unknown character
>15. Guess the randomCode for the character Hscene, it is necessary to adjust the configuration file "./var/var. csv" to enable


### 环境搭建(Running Environment)
1. 下载python3.9并配置环境变量（如果你不会，可以直接搜索Anaconda3安装后会自动配置）
2. 下载并安装pip
3. 在控制台输入这个
```shell
pip install httpx
pip install loguru
pip install pandas
```

>1. Download Python 3.9 and configure environment variables (if you don't know, you can google for Anaconda3 and it will be automatically configured after installation)
>2. Download and install pip
>3. Enter this on the console
```shell
pip install httpx
pip install loguru
pip install pandas
```

### 功能1&2介绍(Features 1 & 2)
这两个功能被绑定在一起

>These two function are bound together

#### 获取角色信息(Obtaining Character Information)
角色资源路径信息，主要有四个项构成charaID,charaFileID,favorability,randomCode。其中charaID加charaFileID合称为角色代码

>The character resource path information mainly consists of four items: charaID, charaFileID, popularity, and randomCode. The charaID and charaFileID are merged into the character code

例如一个角色的资源位置为: https://fruful.jp/img/game/chara/event/334E9Z/100TYVH334_R/images/HCG001.jpg

>For example, the resource path of a character is：https://fruful.jp/img/game/chara/event/334E9Z/100TYVH334_R/images/HCG001.jpg

那么可以拆分为四个部分:

>it can be divided into four parts:

- charaID：334
- charaFileID：E9Z
- favorability：100
- randomCode：TYVH

注1：资源位置即为浏览器所请求的链接地址，此处只展示后半部分。
注2：有特殊情况比如好感度0是角色没有H事件，又如临时工命名不规范导致randomCode为7个字符

>Note 1: The resource path is the link requested by the browser, and only the latter part is shown here.
>Note 2: There are special character, such as favorability：0, means the character without HScene

#### 角色信息缓存文件(Character Information Cache)
在项目中charaMap文件夹下存在charaData.csv文件，此文件包含了大部分角色的资源路径信息。
程序会读取里面的信息并且爬取CG资源存放在当前目录下的output里，以"./角色代码/好感度/"此路径存放。

>There is a charaData.csv file in './charaMap' directory of the project, which contains resource path information for most character.
>The program will read the cache and obtain HScene resources to save them in the './output' of the current directory, the path of "./character code/favorability/".

其中charaID,charaFileID不管你有没有角色，查看别人的角色也可以看到。
而randomCode只有拥有角色且好感度足够后，触发事件可以看到。

>Among, charaID and charaFileID can be seen by everyone, whether you have a character or not.
>However, the randomCode can only be seen when it has a character and has sufficient favorability.

综上，只要知道randomCode，那么直接输入到csv文件内就可不需要大量时间去遍历服务器资源即可获取CG。

>So, if you know the randomCode, entering it into the charaData.csv file, doing so can save some time because without traverse server resources to obtain CG.

一般资源文件代码可以在这里查看：https://docs.google.com/spreadsheets/d/1HhOKUkkUped7tCvwsBDg9-gJrYfLtxV5R43kdAda8_A/edit#gid=0

>The resource file can be viewed here: https://docs.google.com/spreadsheets/d/1HhOKUkkUped7tCvwsBDg9-gJrYfLtxV5R43kdAda8_A/edit#gid=0

非常感谢各位大佬的支持！

>Thank you very much for your contributions！

#### 获取角色立绘(Obtain Character Stand)
如果你想获取角色的立绘，使用FruitPickingStand.py。它会获取服务器角色立绘和高清立绘，并储存在当前目录下outputst，以"./角色代码/普通或高清立绘/进化前或后/"路径存放。

>If you want to obtain a character's Stand, use FruitPickingStand.py. It will obtain character normal-pixel Stand and high-pixel Stand, and save them in the current directory outputst, in the path of "./character code/low or high-pixel image/normal or evolution/".

它只可以遍历charaMap下charaData.csv中存在charaID和charaFileID的角色

>It can only traverse characters with charaID and charaFileID in charaData.csv

### 功能3介绍(Features 3)
功能内嵌在代码中，一般不需要用到，因此不开放修改。如果需要，请见FruitPickingCharaID.py

>The function is embedded in the code and generally does not need to be used, so it is not open for modification. If needed, please see FruitPickingCharaID.py

### 功能4介绍(Features 4)
#### 遍历服务器资源(Traverse Server Resources)
如果不知道角色代码也没关系，使用FruitPickingChara.py可以遍历服务器找出的角色代码。

>If you don't know the character code, it's okay. Using FruitPickingChara.py can traverse the character code found by the server.

如果不知道randomCode也没关系，使用FruitPickingTools.py会通过顺序组合的方式去遍历服务器获取CG。将./var下的var.csv中TRAVERSE_MODE行的value列填1即可开始遍历。

>If you don't know the randomCode, it's okay. Using FruitPickingTools.py will traverse the server through sequential combinations to obtain CG. 'TRAVERSE_MODE' in 'var.csv', set vulue '1' to start traversal.

如果你想遍历某个特定ID的角色的randomCode，将./var下的var.csv中，specifyCharaID填为charaID，specifyCharaFileID，填为charaFileID，var.csv中有示例。

>If you want to traverse the randomCode of a character with a specific ID. Please set value in 'var.csv', specifyCharaID as charaID, specifyCharaFileID as charaFileID, and there are examples in var.csv.

如果你想从某一个特定的randomCode开始往后遍历，将./var下的var.csv中，startRandomCode填为你想要的randomCode，var.csv中有示例。（注意：如果你不想这样做，请留空或填写AAAA）

>If you want to start traversing backwards from a specific randomCode, set value in 'var. csv', fill in the startRandomCode as the randomCode you want, and there are examples in 'var.csv'. (Note: If you do not want to do this, please leave blank or fill in AAAA)

遍历需注意：最好知道randomCode并填入charaData.csv中，否则会花费大量时间去获取角色代码和randomCode（100个线程跑满大约7h遍历一个角色）。

>Note: It is best to know the randomCode and fill it in charaData.csv as a cache, otherwise it will take a lot of time to obtain the randomCode (100 threads running for about 7 hours to traverse one character).

### 附：关于'var.csv'文件说明(Description of 'var.csv' File )
它是一个程序配置文件

>It is a program configuration file, please use Google Translate below


| 变量                | 类型   | 说明                                                            |
| ------------------- | ------ |---------------------------------------------------------------|
| TRAVERSE_MODE       | bool   | 0表示关闭遍历randomCode功能，1表示开启，其他无效                                |
| specifyCharaID      | string | 请输入要遍历角色的CharaID，详细看**获取角色信息**部分的说明                           |
| specifyCharaFileID  | string | 请输入要遍历角色的charaFileID，详细看**获取角色信息**部分的说明                       |
| specifyFavorability | string | 请指定要遍历角色的好感度，可以指定为040或100，留空则两种都遍历                            |
| retryCount          | int    | 每个randomCode发送请求的次数，一般为3~6较好，数值越高越能弥补网络波动从而稳定获得randomCode     |
| startRandomCode     | string | 输入从哪里开始遍历，如果为AAAA，则从AAAA开始到ZZZZ依次遍历，如果为BDFC，则从BDFC开始到ZZZZ依次遍历 |
| silentMode          | bool   | 0表示开启输出遍历日志信息（info级）模式，1表示关闭                                  |

