#!/usr/bin/python
#-*- coding: utf-8 -*-
class Singleton(type):
    
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
            
        except AttributeError: 
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.__instance

class Manager(object):
	
        __metaclass__ = Singleton

	def __init__(self):
		self.__message = {'message': {'text' : ''}}

	def set_message(self, text):
		self.__message['message']['text'] = text

	def get_message(self, text = ''):
                if text == 'json':
		    return self.__message
                else:
                    return self.__message['message']['text']
