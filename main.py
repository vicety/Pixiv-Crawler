
from scrapy.cmdline import execute
import os
import sys

def main():
    print(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(["scrapy", "crawl", "pixivSpider"]) #相当于三个命令

if __name__ == "__main__":
    # prj_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # sys.path.append(prj_dir)
    main()