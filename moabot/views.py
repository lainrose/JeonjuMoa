#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import loads
from multiprocessing import Process, Queue
from threading import Thread

from morpheme import pos_tagger
from spellcheck import spellchecker
from manager import Manager
from weather import Weather
from words import *

manager = Manager()
que = Queue()

def index(request):
    return HttpResponse("Welcome to JeonJu Moa")

def init():
    print('init')
    data = pos_tagger(u'사용자가 입장하였습니다.')
    for word in data:
        print str(word[0])
    print('init exit')

def keyboard_json():
    print('json')
    data = JsonResponse({
            'type' : 'text',
            })
    que.put(data)
    print('json exit')

#GET
def keyboard(request):
    pr1 = Thread(target = init)
    pr2 = Thread(target = keyboard_json)
    pr1.start()
    pr2.start()
    pr2.join()
    result = que.get()
    return result

#POST
@csrf_exempt
def message(request):
    sentence = loads(((request.body).decode('utf-8')))['content']
    print(sentence)
    sentence = spellchecker(sentence)
    words = pos_tagger(sentence)
    text = '현재 날씨 서비스 진행중입니다.\n\n'

    manager.set_message(text)
    for word in words:
        if word in [('날씨', 'Noun'), ('덥다','Adjective'), ('춥다','Adjective')]:
            weather = Weather(words)
        else:
            pass

    if manager.get_message() == text:
        for word in words:
            manager.set_message(manager.get_message() + word[0] + ' ')
    
    return JsonResponse(manager.get_message('json'))
