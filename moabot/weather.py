#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup
from manager import Manager

class Weather:

    __day = [
        ('오늘', 'Noun'), ('내일','Noun'), ('모레', 'Noun'),
        ('글피', 'Noun'), ('월요일', 'Noun'), ('화요일', 'Noun'),
        ('수요일', 'Noun'), ('목요일', 'Noun'), ('금요일', 'Noun'),
        ('토요일', 'Noun'), ('일요일', 'Noun')
    ]
    __area = [
        ('진북동', 'Noun'), ('인후동', 'Noun'), ('덕진동', 'Noun'),
        ('금암동', 'Noun'),('팔복동', 'Noun'), ('산정동', 'Noun'),
        ('금', 'Noun'), ('상동', 'Noun'),('우아동', 'Noun'), 
        ('호성동', 'Noun'), ('전', 'Noun'), ('미동', 'Noun'),
        ('송천동', 'Noun'), ('반월동', 'Noun'), ('화전동', 'Noun'),
        ('용', 'Noun'), ('정동', 'Noun'), ('성덕동', 'Noun'),
        ('원동', 'Noun'), ('동산동', 'Noun'),('고랑', 'Noun'),
        ('동', 'Noun'), ('여의동', 'Noun'), ('만', 'Noun'), 
        ('성동', 'Noun'), ('장동', 'Noun'), ('도도', 'Noun'),
        ('동', 'Noun'), ('강', 'Noun'), ('흥동', 'Noun'),
        ('도덕', 'Noun'), ('동', 'Noun'),('남', 'Noun'),
        ('정동', 'Noun'), ('인후', 'Noun'), ('조촌동', 'Noun')
    ]

    __match_area = '전주시'
    __match_day = '오늘'
    manager = Manager()
  
    def __init__(self, words):
        self.words = words
	self.times = []
	self.scripts = []
	self.temps = []
	self.precips = []
        self.today_script = ''
        self.today_temp = ''
        self.today_temp1 = ''
	self.script_keys = {'화창' : '(해)',
                        '맑음' : '(해)',
                        '구름' : '(구름)',
                        '흐림' : '(구름)(구름)',
                        '비' : '(비)',
                        '소나기' : '(비)',
                        '눈' : '(눈)',
                        '밤' : '(잘자)',
                        }   
        self.except_keys = ['비', '소나기']
	self.convo()

    def convo(self):
        for word in self.words:
            key = word[0]
            pos = word[1]
            
            if word in self.get_area():
                self.__match_area = key

            elif word in self.get_day():
                self.__match_day = key

        self.manager.set_message(
            self.parse()
        )

    def get_area(self):
        return self.__area

    def get_day(self):
        return self.__day

    def parse(self):
	self.html = urllib.urlopen(
    		'http://weather.com/ko-KR/weather/hourbyhour/l/KSXX0205:1:KS')
        self.soup = BeautifulSoup(self.html, 'lxml')
        
	self.parse_times = self.soup.find_all(class_ = 'dsx-date')
	self.parse_scripts = self.soup.find_all(
    				class_ = 'hidden-cell-sm description')
	self.parse_temps = self.soup.find_all('td', {'class' : 'temp'})
	self.parse_precips = self.soup.find_all('td', {'class' : 'precip'})

        self.html = urllib.urlopen(
                    'http://weather.com/ko-KR/weather/today/l/KSXX0205:1:KS')
        self.soup = BeautifulSoup(self.html, 'lxml')

        self.today_script = self.soup.find('span', class_ = 'today-wx-descrip').string
        self.today_script = self.today_script.split('. ')
        self.today_temp = self.today_script[1].split(' ')[0].encode('utf-8')
        self.today_temp1 = self.today_script[1].split(' ')[1].encode('utf-8')
        self.today_script = self.today_script[0]
        
	for time, script, temp, precip in zip(
		                    self.parse_times, self.parse_scripts,
				    self.parse_temps, self.parse_precips):

	    time = time.string.split(':')[0].encode('utf-8')
	    script = script.span.string.encode('utf-8')
	    temp = str(temp.span).split(
                            '<sup>')[0].split(
                            '<span class="">')[1].encode('utf-8')
	    precip = str(precip.div.span.next.span).split(
                            '<span class="percent-symbol">')[0].split(
                            '<span>')[1].encode('utf-8')

	    self.times.append(int(time))
	    self.scripts.append(script)
	    self.temps.append(temp)
	    self.precips.append(precip)

        return self.process()

    def process(self):
        self.message = self.__match_day + ' ' + self.__match_area + ' ' +\
                        '날씨는 ' + self.today_script + '이며,\n예상 ' +\
                        self.today_temp + ' 기온은 ' + self.today_temp1 +\
                        ' 입니다.\n'

	for idx, (time, script, temp, precip) in enumerate(zip(
				    self.times, self.scripts,
				    self.temps, self.precips)):
            if idx == 0:
                pass
            elif idx % 2 == 0:
                continue
            
	    night_times = range(20,24) + range(0,6)
            for key in self.script_keys:
                if key in script:
                    if time in night_times:
                        if key not in self.except_keys:
                            script = self.script_keys['밤']
                    else:
                        script = self.script_keys[key]
            
            if not idx:
                time = '지금: '
	    elif time in range(0, 12):
		time = '오전 ' + str(time) + '시: '
	    else:
                if time == 12:
                    pass
                else:
                    time = time - 12
		time = '오후 ' + str(time) + '시: '

            temp = temp + '℃ '

	    if int(precip) in range(0,10):
		precip = ''
	    else:
		precip = ' (땀) ' + precip + '%'

	    self.message += time + script + ' ' + temp + precip + '\n\n'
			
	return self.message

if __name__ == "__main__":
    w = Weather([('날씨','Noun')])
