# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return HttpResponse("Welcome to JeonJu Moa")

#GET
def keyboard(request):
    return JsonResponse({
            'type' : 'buttons',
            'buttons' : ['사용법']
            })
#POST
@csrf_exempt
def message(request):
        message = json.loads(((request.body).decode('utf-8')))['content']
        if message == '날씨':
           return JsonResponse({
                'message': {
                'text': '어딘지를 말해줘야지'},
                }) 

        return JsonResponse({
                'message': {
                'text': message},
                })

