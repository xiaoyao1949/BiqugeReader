# BiqugeReader

**环境:**

- python3.X



**软件功能：**

- 爬取[笔趣阁](https://www.biquge.info/)的所有小说
- 每本小说生成词云图片
- 每本小说通过百度语音合成api生成有声读物



**每个py模块的作用：**

- biqugeSpider.py 负责爬取所有小说的名称和页面链接，生成形如[(书名1,地址1),(书名2,地址2),(..........)]的列表
- Declaimer.py 负责封装百度语音合成api。构造Declaimer类，使其可以输入文本，输出音频文件。
- Mp3Gen.py 负责生成单本小说的音频文件。
- NovelSpider.py 负责爬取单本小说，生成对应的txt文件
- sites.py 用来存储不同网站的解析策略
- WordCloudGen.py 负责生成单本小说的词云图片
- director.py 是整个程序的入口，负责调度其他所有模块



**软件如何使用？**

​	直接用python解释器执行director.py即可

​	如果出现错误，检查一下依赖的库是否安装好了。





