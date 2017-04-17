#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from konlpy.tag import Twitter
from konlpy.utils import pprint
import jpype

twitter = Twitter()

def get_unicode(parm):
    return unicode(parm, 'utf8')

def get_morphs(parm):#형태소 list를 반환한다.
    return twitter.morphs(get_unicode(parm))
    
def get_nouns(parm):#명사 list를 반환한다.
    return twitter.nouns(get_unicode(parm))

def get_phrases(parm):# 문장에서 가능한 의미 덩이들의 list를 반환한다.
    return twitter.phrases(get_unicode(parm))
    
def get_pos(parm):#stem – If True, stem tokens.
    jpype.attachThreadToJVM()
    pos = twitter.pos(parm, norm=True, stem=True)
    jpype.detachThreadFromJVM()

    return pos

if __name__ == "__main__":
    m = Morpheme()

    #for word in words:
    i = raw_input("키워드 입력하세용 : ")
    pprint(m.get_pos(i))
