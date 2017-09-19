# Pixiv-Crawler
这是一个scrapy框架的爬虫
基于`win10`、`Python 3.6.2 64位`、`Scrapy 1.4.0`开发，其他环境下未测试

### 功能
* 我的收藏导出
* 画师作品导出
* 搜索图片导出
* 所有导出均支持图片大小筛选、收藏量筛选（画师作品导出不支持）
* 指定导出位置

### 未完成部分
* 日榜导出
* 增加一些其他的插画网站
* 一些细节



### requirements
* python
* scrapy
* requests 
* pillow 
* pypiwin32 // 可能需要 
* 如果还缺少什么，一般直接pip install就可以了

### 使用方法
先在`settings.ini`进行配置，然后在`main.py`文件目录下进入cmd
	python main.py
#### Setting文件配置说明
	[PRJ]  
	TARGET = COLLECTION  // 三种执行方式之一 COLLECTION  ARTIST SEARCH 对应 收藏导出 画师作品导出 搜索内容导出 
	ACCOUNT = 
	PASSWORD = 
	
	[IMG]
	MIN_WIDTH = 0	//图片筛选条件
	MIN_HEIGHT = 0
	MIN_FAV = 0 
	STORE_PATH = C:\example\images  // 图片储存目录，默认为工程目录下的image,
	R18 = False //仅R18

	[ART]
	ID = 123456 // 画师ID

	[SRH]
	TAGS = TAG_A TAG_B ... // 搜索内容
	
	[DAILY] 

###版本日志
####V1.1
修复搜索时日语编码问题
修改了setting文件结构，可以配置默认账号密码
修复了打印日志上的一些问题
####V1.0



最后，初次写爬虫，写得不是很好，有任何问题欢迎指教