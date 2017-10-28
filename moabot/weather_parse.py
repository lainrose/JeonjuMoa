# -*- coding: utf-8 -*-

import urllib2
import json
import threading 

api_key = '8d821f5e48621cf9'
days_keys = {'Mon' : '월', 'Tue' : '화', 'Wed' : '수',
                'Thu' : '목', 'Fri' : '금', 'Sat' : '토',
                'Sun' : '일'} 
conditions_keys = {'Rain' : '(비)', 'Cloudy' : '(구름)',
                    'Overcast' : '(구름)', 'Clear' : '(해)',
                    'Thunderstorm' : '(비)뇌우'}

def hourly10day():

    html = 'http://api.wunderground.com/api/8d821f5e48621cf9/' +\
            'hourly10day/q/KR/Jeonju.json'
    u = urllib2.urlopen(html)
    json_string = u.read()
    parsed_json = json.loads(json_string)['hourly_forecast']

    with open('weather_data.py', 'w') as f:
        data = '# -*- coding: utf-8 -*-\n\n' +\
                'def get_hourly10day():\n' +\
                '\treturn hourly10day\n\n' +\
                'hourly10day = [\n'
        f.write(data)
        for i in parsed_json:
        # 요일 날짜 시간 AM 온도 이슬점 날씨 강우량
            data = {}
            data['day'] = i['FCTTIME']['weekday_name_abbrev'].encode('utf-8')
            for key in days_keys:
                if key in data['day']:
                    data['day'] = days_keys[key]

            data['date'] = i['FCTTIME']['mday'].encode('utf-8')
            data['hour'] = i['FCTTIME']['hour'].encode('utf-8')

            data['ampm'] = i['FCTTIME']['ampm'].encode('utf-8')
            if data['ampm'] == 'AM':
                data['ampm'] = '오전'
            else:
                data['ampm'] = '오후'

            data['temp'] = i['temp']['metric'].encode('utf-8')

            data['cond'] = i['condition'].encode('utf-8')
            for key in conditions_keys:
                if key in data['cond']:
                    data['cond'] = conditions_keys[key]

            data['precip'] = i['pop'].encode('utf-8')

            f.write('{')
            for j in data:
                f.write("'" + str(j) +"' : '" + data[j] + "',\n")
            f.write('},\n')
        f.write(']')

    u.close()

def forecast10day():
    html = 'http://api.wunderground.com/api/8d821f5e48621cf9/' +\
            'forecast10day/q/KR/Jeonju.json'

    u = urllib2.urlopen(html)
    json_string = u.read()
    parsed_json = (json.loads(json_string)
		        ['forecast']['simpleforecast']['forecastday'])

    with open('weather_data.py', 'a') as f:
        data = '\n\n' +\
                'def get_forecast10day():\n' +\
                '\treturn forecast10day\n\n' +\
                'forecast10day = [\n'
        f.write(data)
        for i in parsed_json:
	    data = {}
    	    data['date'] = i['date']['day']

            data['day'] = i['date']['weekday_short'].encode('utf-8')
            for key in days_keys:
                if key in data['day']:
                    data['day'] = days_keys[key]

            data['high'] = i['high']['celsius'].encode('utf-8')
            data['low'] = i['low']['celsius'].encode('utf-8')

            data['cond'] = i['conditions'].encode('utf-8')
            for key in conditions_keys:
                if key in data['cond']:
                    data['cond'] = conditions_keys[key]
                    
            data['precip'] = i['pop']
            f.write('{')
            for j in data:
                f.write("'" + str(j) +"' : '" + str(data[j]) + "',\n")
            f.write('},\n')
        f.write(']')

    u.close()

end = False
i = 0 
def execute(second=300):
    global end
    global i
    if end:
        return
    # TODO
    hourly10day()
    forecast10day()
    i += 1
    print("weather_parse.py : " + str(i))

    threading.Timer(second, execute).start()

if __name__ == "__main__":
    execute()
