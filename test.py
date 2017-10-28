#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json

def send(text):
    url = "http://52.79.210.110:8000/message"
    text = {"user_key" : "I5MENw6y-heE", "type" : "text", "content" : text}
    request = json.dumps(text)
    response = requests.post(url, data = request)
    print(response.text)
    message = json.loads(response.text)['message']['text']
    print(message)

if __name__ == "__main__":
    while(True):
        input = raw_input("Message : ")
        result = send(input)
