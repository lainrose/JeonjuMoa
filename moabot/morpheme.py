#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from konlpy.tag import Twitter
from konlpy.utils import pprint
import jpype
import time

twitter = Twitter()

def get_unicode(parm):
    return unicode(parm, 'utf8')

    """ 
    konlpy모듈이 JVM으로 wrapper을 이용하기 때문에 
    파이썬 장고 서버구동과 같이 하게되면 2개의 스레드
    이기 때문에 멀티스레드로 돌려줘야한다.
    jpype.attachThreadToJVM()코드가 멀티스레드를 지원
    해주는 코드인 것 같다. 안해주면 JVM FATAL ERROR 발생 
    """

#형태소 list를 반환한다.
def get_morphs(parm):
    jpype.attachThreadToJVM()
    morphs = twitter.morphs(get_unicode(parm))
    jpype.detachThreadFromJVM()
    
    return morphs

#명사 list를 반환한다.
def get_nouns(parm):#명사 list를 반환한다.
    jpype.attachThreadToJVM()
    nouns = twitter.nouns(get_unicode(parm))
    jpype.detachThreadFromJVM()

    return nouns

# 문장에서 가능한 의미 덩이들의 list를 반환한다.
def get_phrases(parm):#
    jpype.attachThreadToJVM()
    phrases = twitter.phrases(get_unicode(parm))
    jpype.detachThreadFromJVM()

    return phrases
   
#return list of tuple [(단어<str>, 품사<str>)]
def pos_tagger(parm):
    start = time.time()

    jpype.attachThreadToJVM()
    pos = twitter.pos(parm, norm=True, stem=True)
    jpype.detachThreadFromJVM()

    end = time.time() - start
    print("======pos_tagger_time : " + str(round(end, 2)))

    return pos

if __name__ == "__main__":
    i = raw_input("키워드 입력하세용 : ")
    pprint(pos_tagger(i))
