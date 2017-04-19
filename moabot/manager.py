#!/usr/bin/python
#-*- coding: utf-8 -*-

class Manager:
	
	def __init__(self):
		self.__message = {'message': {'text' : ''}}

	def set_message(self, text):
                print(text)
		self.__message['message']['text'] = text
                print(self.__message)

	def get_message(self):
		return self.__message

