#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import re
import requests
import time

def spellchecker(text):
    
    url = "https://m.search.naver.com/p/csearch/dcontent/spellchecker.nhn"
    params = { 
        '_callback': 'window.mycallback',
        'q': text,
    }   
    headers = { 
        'User-Agent': 'Mozilla/5.0'
    }   

    response = requests.get(url, params = params, headers = headers).text
    response = response.replace(params['_callback'] + '(', '') 
    response = response.replace(');', '') 
    js = json.loads(response)
    result = js['message']['result']['html']
    result = re.sub(r'<\/?.*?>', '', result)

    return result

if __name__ == "__main__":
    input = raw_input("맞춤법을 검사할 문장을 입력하세요.\n")
    print(spellchecker(input))
