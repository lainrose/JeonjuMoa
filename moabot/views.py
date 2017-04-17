#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jpype

from morpheme import get_pos

def index(request):
    return HttpResponse("Welcome to JeonJu Moa")

#GET
def keyboard(request):
    return JsonResponse({
            'type' : 'buttons',
            "buttons" : ['사용법']
            })
#POST
@csrf_exempt
def message(request):
    content = json.loads(((request.body).decode('utf-8')))['content']

    if content == '사용법':
        return JsonResponse({
            'message' : {'text' : u'그냥 아무말이나 쓰세요'}
            })
    else:
        words = get_pos(content)
        message = ''
        for word in words:
            message += word[0] + ' [' + word[1] + ']\n'

        return JsonResponse({
            'message': {'text': message},
            })
