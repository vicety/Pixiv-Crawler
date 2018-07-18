import os
import configparser
import codecs

# import sys
# sys.path.append('../')

class PixivError(Exception):
    pass


class UnmatchError(PixivError):
    def __init__(self, msg):
        super(UnmatchError, self).__init__()
        self.args = (msg,)

def settings_assert():
    prj_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    os.chdir(prj_dir)
    cf = configparser.ConfigParser()
    try:
        cf.read_file(codecs.open("../settings.ini", 'r', 'utf-8-sig'))
    except Exception as e:
        print("配置文件格式有误 error: {0}".format(e))
        exit(-1)
    PRJ_OPTIONS = [
        'SEARCH', 'COLLECTION', 'COLLECTION_PRIVATE', 'ARTIST', 'DAILY'
    ]

    assert cf.get('PRJ', 'TARGET') in PRJ_OPTIONS, 'Check whether your PRJ option is SEARCH COLLECTION ARTIST or DAILY'
    assert (cf.getint('DAILY', 'FROM') >= 1 and cf.getint('DAILY', 'FROM') <= 500 and cf.getint('DAILY', 'TO') >= 1 and cf.getint('DAILY', 'TO')), 'daily rank selection out of range (from 1 to 500)'
