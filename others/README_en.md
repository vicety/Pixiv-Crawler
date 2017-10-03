# Pixiv-Crawler
A spider build on scrapy
developed on `win10`、`Python 3.6.2 64bits`、`Scrapy 1.4.0`，not yet tested in other environment

### Functions
* export Bookmarks
* export paintings from certain artist
* export paintings from tags
* export paintings from daily ranking
* all exporting supports simple image-size filtering
* can assign the exporting directory

### Unfinished
* supporting some similar websites
* optimize some details

### Requirements
* python
* scrapy
* requests 
* pillow 
* pypiwin32 // maybe not necessary 
* if missing any other things, just "pip install" 

### Usage
configure `settings.ini`，then enter cmd at the directory of `main.py` <br>
input	`python main.py`
#### Instruction of "setting.ini"
	[PRJ]  
	TARGET = COLLECTION  // one of the following four choices COLLECTION  ARTIST SEARCH DAILY correspond respectively to Bookmarks/Artists' paintings/Search by tags/Daily ranking exporting
	ACCOUNT = 
	PASSWORD = 
	
	[IMG] 
	MIN_WIDTH = 0	//image filtering
	MIN_HEIGHT = 0
	MIN_FAV = 0		
	STORE_PATH = C:\example\images		// image storing directory，"image" folder at the project directory by default
	R18 = False		//whether download only the R18 paintings
	MULI_IMG_ENABLED = False	// whether download those with multiple paintings

	[ART]	// not limited by the MIN_FAV at IMG
	ID = 123456 // artist ID，seperate by space if more than one artists

	[SRH]
	TAGS = TAG_A TAG_B ... // searching tags
	
	[DAILY] // not limited by the MIN_FAV at IMG

### 提醒
由于P站限制，搜索功能最多搜索1000页，可以通过添加类似“1000users入り”（不含引号）这样的tag来缩小搜索范围	

### 版本日志
#### V1.2
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