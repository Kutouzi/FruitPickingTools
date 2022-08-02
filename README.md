## FruitPickingTools
一个可爬取ふるーつふるきゅーとCG的工具，扩展后也可以用来爬取其他如立绘等资源

目前有的功能：
1. 获取角色CG和MV储存于“./output”
2. 获取角色立绘和高清立绘
3. 猜测未知角色ID
4. 猜测角色Hscene特殊码

### 环境搭建
1. 下载python3.9并配置环境变量（如果你不会，可以直接搜索Anaconda3安装完直接配置好）
2. 下载并安装pip
3. 在控制台输入这个
```shell
pip install httpx
pip install loguru
pip install pandas
```
### 工具使用

#### 获取角色信息
角色资源路径信息，主要有四个项构成charaID,charaFileID,favorability,randomCode。其中charaID加charaFileID合称为角色代码。

例如一个角色的资源位置为：https://fruful.jp/img/game/chara/event/334E9Z/100TYVH334_R/images/HCG001.jpg。

那么可以拆分为四个部分。

- charaID：334
- charaFileID：E9Z
- favorability：100
- randomCode：TYVH

注1：资源位置即为浏览器所请求的链接地址，此处只展示后半部分。
注2：有特殊情况比如0是角色没有H事件，又如临时工命名不规范导致randomCode为7个字符

#### 角色信息缓存文件
在项目中charaMap文件夹下存在charaData.csv文件，此文件包含了大部分角色的资源路径信息。
程序会读取里面的信息并且爬取CG资源存放在当前目录下的output里，以"./角色代码/好感度/"此路径存放。

其中charaID,charaFileID不管你有没有角色，查看别人的角色也可以看到。
而randomCode只有拥有角色且好感度足够后，触发事件可以看到。

综上，只要知道randomCode，那么直接输入到csv文件内就可不需要大量时间去遍历服务器资源即可获取CG。

一般资源文件代码可以在这里查看：https://docs.google.com/spreadsheets/d/1HhOKUkkUped7tCvwsBDg9-gJrYfLtxV5R43kdAda8_A/edit#gid=0

非常感谢各路大佬的支持！

#### 遍历服务器资源
如果不知道角色代码也没关系，使用FruitPickingChara.py可以遍历服务器找出的角色代码。

如果不知道randomCode也没关系，使用FruitPickingTools.py会通过顺序组合的方式去遍历服务器获取CG。将./var下的var.csv中TRAVERSE_MODE行的value列填1即可开始遍历。

如果你想遍历某个特定ID的角色的randomCode，将specifyCharaID填为charaID，specifyCharaFileID，填为charaFileID，var.csv中有示例。

遍历需注意：最好知道randomCode并填入charaData.csv中，否则会花费大量时间去获取角色代码和randomCode（100个线程跑满大约13h遍历一个角色）。

#### 获取角色立绘
如果你想获取角色的立绘，使用FruitPickingStand.py。它会获取服务器角色立绘和高清立绘，并储存在当前目录下outputst，以"./角色代码/普通或高清立绘/进化前或后/"路径存放。

它只可以遍历charaMap下charaData.csv中存在charaID和charaFileID的角色