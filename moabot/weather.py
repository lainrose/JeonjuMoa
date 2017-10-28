#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from manager import Manager
from words import *
from weather_data import *
from weather_say import *

class Weather:

    __match_area = '전주시'
    __match_day = '오늘'
    f_next = False
    f_prev = False
    manager = Manager()
    hdays = get_hourly10day()
    fdays = get_forecast10day()
  
    def __init__(self, words):
        self.words = words
        self.day_keys = {'월요일' : '월', '화요일' : '화',
                            '수요일' : '수', '목요일' : '목',
                            '금요일' : '금', '토요일' : '토',
                            '일요일' : '일'}
        self.except_keys = ['(비)', '(구름)', '(비)뇌우']
        self.next_keys = ['다음', '돌아오다']
        self.prev_keys = ['어제', '저번']
        self.res_message = ''
	self.convo()

    def convo(self):
        self.istoday = True
        
        for word in self.words:
            pos = str(word[1])
            word = str(word[0])
            if word in self.next_keys:
                self.f_next = True
            if word in self.prev_keys:
                self.f_prev = True
            
            if word in get_area():
                self.__match_area = get_area()[word]

            if word in get_day():
                self.__match_day = get_day()[word]
                self.res_message += self.fday()
                print self.res_message

                if word in ['오늘']:
                    self.res_message += self.hday()
                if not self.res_message == '':
                    self.istoday = False

            if word in self.prev_keys:
                self.res_message = "이전 날씨는 중요하지 않아요.."
                self.istoday = False
                break
            if word in ['덥다']:
                self.res_message = "더울까요? 날씨를 물어보세요~"
            if word in ['춥다']:
                self.res_message = "추울까요? 날씨를 물어보세요~"

        if self.istoday:    
            self.res_message += self.hday()
        self.manager.set_message(self.res_message)

    def fday(self):
        self.origin_mssg = self.__match_day + ' ' + self.__match_area + ' ' +\
                        weather_say(0) + '\n\n'
        self.copy_mssg = self.origin_mssg
        mday = self.__match_day.split('요일')[0]
        print(mday)
        f_next_week = False

        for idx, f in enumerate(self.fdays):
            date = f['date']
            day = f['day']
            cond = f['cond']
            high = f['high']
            low = f['low']
            precip = f['precip']
            blank = '\n'

            if int(precip) in range(0,11):
                precip = ''
            else:
                precip = '(땀)' + precip + '%'

            if ((mday in ['내일'] and idx == 1) or
                (mday in ['모레'] and idx == 2) or
                (mday in ['글피'] and idx == 3) or
                (mday in ['주말'] and day in ['토', '일'])):
                self.copy_mssg += day + '(' + date + ') ' + cond + ' ' +\
                                high + '°/' + low + '℃  ' + precip + blank

            if mday in day:
                if self.f_next:
                    pass

                self.res_message = ''
                self.copy_mssg = self.origin_mssg
                self.copy_mssg += day + '(' + date + ') ' + cond + ' ' +\
                                high + '°/' + low + '℃  ' + precip + blank

            elif mday in ['주']:

                if idx % 2 == 0:
                    blank = '\n\n'

                #다음 주
                if self.f_next:
                    if not idx:
                        self.copy_mssg = '다음 ' + self.copy_mssg +\
                                                    weather_say(3) + '\n\n'
                        continue
                    if day in ['월']:
                        f_next_week = True
                    if f_next_week:
                        self.copy_mssg += day + '(' + date + ') ' + cond + ' ' +\
                                        high + '°/' + low + '℃  ' + precip + blank
                        if day in ['일']:
                            break
                #이번 주
                else:
                    if not idx:
                        self.copy_mssg = '이번 ' + self.copy_mssg

                    if day in ['월']:
                        break
                    self.copy_mssg += day + '(' + date + ') ' + cond + ' ' +\
                                    high + '°/' + low + '℃  ' + precip + blank

            elif mday in ['달']:
                if self.f_next:
                    self.copy_mssg = "다음 달은 무리랍니다."

                else:
                    if idx == 0:
                        self.copy_mssg = "이번 " + self.copy_mssg +\
                                            weather_say(2) + '\n\n'
                    if idx % 2 == 0 :
                        blank = ' | '
                    if day == '일':
                        blank = '\n\n'
                    self.copy_mssg += day + '(' + date + ') ' + cond + ' ' +\
                                    high + '℃ ' + blank
        self.copy_mssg += '\n'
        print self.res_message
        return self.copy_mssg


    def hday(self):
        self.message = self.__match_day + ' ' + self.__match_area + ' ' +\
                        weather_say(1) + '\n\n'

        for idx, h in enumerate(self.hdays):
            hour = h['hour']
            temp = h['temp']
            ampm = h['ampm']
            precip = h['precip']
            cond = h['cond']
            blank = '\n'
            
	    night_times = range(20,24) + range(0,6)
            if int(hour) in night_times:
                if cond not in self.except_keys:
                    cond = '(잘자)'
            
            if h['ampm'] == '오후':
                hour_int = int(hour)
                if hour_int == 12:
                    pass
                else:
                    hour = str(hour_int - 12)

	    if int(precip) in range(0,11):
		precip = ''
            else:
                precip = '(땀)' + precip + '%'
            
            if (idx+1) % 4 in [0, 1] :
                blank = '\n\n'

            if ampm == '오전' and (hour in ['1']) and idx != 0:
                break
            elif idx % 2 == 0:
                if idx == 0:
                    self.message += '지금' + ' ' + ' : ' + ' ' + cond +\
                                    ' ' + temp + '℃  ' + precip + blank
                    continue
                elif hour in ['0']:
                    pass
                else:
                    continue
	    self.message += ampm + ' ' + hour + '시 : ' + ' ' + cond + ' ' +\
                            temp + '℃  ' + precip + blank

	return self.message

if __name__ == "__main__":
    w = Weather([('날씨','Noun')])
