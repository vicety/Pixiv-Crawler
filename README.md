# pixiv-beta
	这是一个scrapy框架的爬虫

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

基于`win10`、`Python 3.6.2`、`Scrapy 1.4.0`开发，其他环境下未测试

### requirements
* python
* scrapy 
* pillow 
* pypiwin32 
* 剩下忘了……缺什么直接pip安装就行了

### 使用方法
程序入口为`main.py`，运行配置均在`settings.conf·中设置
#### Setting文件说明
	[PRJ]  
	TARGET = COLLECTION  // 执行方式（见下） 

	[IMG]
	MIN_WIDTH = 0	//图片筛选条件
	MIN_HEIGHT = 0
	MIN_FAV = 0 
	STORE_PATH = YOUR_DIR  // 图片储存目录，默认为工程目录下的image

	[ART]
	ID = 123456 // 画师ID

	[SRH]
	TAGS = TAG_A TAG_B ... // 搜索内容
	R18 = False

	[DAILY] 

对于执行方式 COLLECTION 收藏导出 ARTIST 画师作品导出 SEARCH 搜索内容导出


最后，初次写爬虫，写得不是很好，有任何问题欢迎指教