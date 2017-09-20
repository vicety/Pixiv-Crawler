# Pixiv-Crawler
这是一个scrapy框架的爬虫
基于`win10`、`Python 3.6.2 64位`、`Scrapy 1.4.0`开发，其他环境下未测试

### 功能
* 我的收藏导出
* 画师作品导出
* 搜索图片导出
* 日榜导出
* 所有导出均支持图片大小筛选
* 指定导出位置

### 未完成部分
* 增加一些其他的插画网站
* 一些细节
* 想到再加

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
	TARGET = COLLECTION  // 四种执行方式之一 COLLECTION  ARTIST SEARCH DAILY 对应 收藏导出 画师作品导出 搜索内容导出 日榜导出
	ACCOUNT = 
	PASSWORD = 
	
	[IMG] 
	MIN_WIDTH = 0	//图片筛选条件
	MIN_HEIGHT = 0
	MIN_FAV = 0		
	STORE_PATH = C:\example\images		// 图片储存目录，默认为工程目录下的image
	R18 = False		//仅下载R18
	MULI_IMG_ENABLED = False	// 是否下载图集

	[ART]	// 不受IMG中的收藏数限制
	ID = 123456 // 画师ID，多个以空格分隔

	[SRH]
	TAGS = TAG_A TAG_B ... // 搜索内容
	
	[DAILY] // 不受IMG中的收藏数限制

### 版本日志
#### V1.2
增加了日榜导出功能
增加了settings文件格式检查
#### V1.1
可以同时添加多个画师<br>
修复搜索时日语编码问题<br>
修改了setting文件结构，可以配置默认账号密码<br>
修复了打印日志上的一些问题<br>
#### V1.0
初始版本


最后，初次写爬虫，写得不是很好，有任何问题欢迎指教