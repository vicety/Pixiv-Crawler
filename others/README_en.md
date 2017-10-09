# Pixiv-Crawler
[中文版](README.md)<br>
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

### Tips
Causing by the restriction of the website，the searching function can search up to 1000 pages，however, its recommanded to add a tag like “1000users入り”（without quotes）to minimize the range of searching	

### Version
#### V1.2
Added daily ranking exporting<br>
Added setting file format inspection<br>
#### V1.1
Can add more than one artists at a time<br>
Fixed a bug caused by Japanese encoding<br>
Reconstruct the setting file，setting default account and password available<br>
Fixed some problems occured when printing the logs<br>
#### V1.0
Initial version<br>

Lastly, its my first time writing a spider, if any questions or problem, its welcomed to contact me.