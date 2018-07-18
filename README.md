# Pixiv-Crawler
这是一个scrapy框架的爬虫
基于`win10`、`Python 3.6.2 64位`、`Scrapy 1.4.0`开发<br>
在`Ubuntu 16.04`、`Python 3.5.2 64位`<br>
`Archlinux`、`Python 3.6.2 64位`<br>
`win10`、`Python 3.6.2`、`Python 3.5.2`下测试成功

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
* 多图片网页暂不能命名文件

### requirements
* python
* scrapy
* requests 
* pillow 
* pypiwin32 // 可能需要
* imageio //下载gif时需要
* 如果还缺少什么，一般直接pip install就可以了

### 使用方法
先在`settings.ini`进行配置，然后在`main.py`文件目录下进入cmd
	python main.py
#### Setting文件配置说明
	[PRJ]  
	/* 
	四种执行方式之一
	COLLECTION  收藏
	COLLECTION_PRIVATE 非公开收藏
	ARTIST 画师作品
	SEARCH 搜索内容
	DAILY 日榜
	*/
	TARGET = COLLECTION  
	ACCOUNT = 
	PASSWORD = 
	
	[IMG] 
	MIN_WIDTH = 0	//图片筛选条件
	MIN_HEIGHT = 0
	MIN_FAV = 0		
	STORE_PATH = ./images		// 图片储存目录，默认为工程目录下的image
	R18 = False		//仅下载R18
	MULI_IMG_ENABLED = False	// 是否下载图集

	[ART]	// 不受IMG中的收藏数限制
	ID = 123456 // 画师ID，多个以空格分隔

	[SRH]
	TAGS = TAG_A TAG_B ... // 搜索内容
	
	[DAILY] // 不受IMG中的收藏数限制

### 其他
* 如果在浏览器无法登陆pixiv或爬取时速度较慢，可以尝试[修改host文件](./others/host.txt)
* 由于P站限制，搜索功能最多搜索1000页，可以通过添加类似“1000users入り”（不含引号）这样的tag来缩小搜索范围	
* 请确保用户语言为简体中文
* 如果提示setting文件编码问题，请尝试在编辑settings.ini文件时使用utf-8编码

### 版本日志
#### V1.2.3
增加对COLLECTION中爬取内容的追踪，过滤曾经爬过的图片，以支持个人收藏的快速更新<br>
对文件存储结构和打印日志部分的优化<br>
支持爬取非公开收藏
#### V1.2.2
应对Pixiv的页面改动，修改了部分数据的获取接口<br>
由于找不到接口，不再支持Gif文件（如果找到了，还请通知一下）<br>
#### V1.2.1
指定目录不存在时自动创建<br>
增加图集的下载和Title抓取<br>
同时抓取图片相关信息，以json格式存储<br>
存储cookie以自动登录
#### V1.2.0
增加了日榜导出功能<br>
增加了settings文件格式检查<br>
#### V1.1
可以同时添加多个画师<br>
修复搜索时日语编码问题<br>
修改了setting文件结构，可以配置默认账号密码<br>
修复了打印日志上的一些问题<br>
#### V1.0
初始版本<br>


最后，初次写爬虫，写得不是很好，有任何问题欢迎指教
