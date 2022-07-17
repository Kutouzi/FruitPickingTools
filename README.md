## FruitPickingTools
一个可爬取ふるーつふるきゅーとCG的工具
### 环境搭建
1. 下载python3.9并配置环境变量（如果你不会，可以直接搜索Anaconda3安装完直接配置好）
2. 下载并安装pip
3. 在控制台输入这个
```shell
pip install httpx
```
### 工具使用

#### 获取角色信息
在项目中charaMap文件夹下存在charaData.csv文件，你可以用excel打开它编辑。
程序会读取里面的内容并且爬取cg资源。

主要有四个列构成charaID,charaFileID,favorability,randomCode

例如一个角色的资源位置为：334E9Z/100TYVH334_R。那么可以拆分为四个部分。

注：资源位置即为浏览器所请求的链接地址，此处只展示后半部分。

- charaID：334
- charaFileID：E9Z
- favorability：100
- randomCode：TYVH

其中charaID,charaFileID不管你有没有角色，查看别人的角色也可以看到。
而randomCode只有拥有角色且好感度足够后，触发事件可以看到。

因此，只要知道randomCode，那么直接输入到csv文件内就可不需要大量时间去遍历服务器资源即可获取CG。

#### 遍历服务器资源

如果没有角色也没关系，由于randomCode是四个A-Z的字母组成，程序会通过顺序组合的方式去遍历服务器获取CG。

输入charaID和charaFileID即可开始遍历，此过程非常耗时间。

