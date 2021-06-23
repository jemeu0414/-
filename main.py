import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import datetime
import time

find = 'hyunsang'
r = requests.get('https://pastebin.com/raw/d4Tu9uGp') #데이터를 읽어드릴 url을 불러와 저장합니다.
r = r.text #url의 내용을 출력할수 있도록 변환해줍니다.
expried = re.search(find + '(.*)days', r).group(1) #변수 find 와 days 사이의 문자열들을 불러옵니다.
expried = expried.replace("=","") #날짜만 가져올수있도록 변수 find 뒤에 날짜를 구분하는 = 를 지워줍니다.
expried = datetime.datetime.strptime(expried, '%Y-%m-%d %H:%M:%S') #문자열 타입으로 되어있는 날짜를 날짜타입으로 변경해줍니다.

noexpired = '5555-01-01 01:01:01' #5555년 뒤로 지나가면 기간을 무제한으로 출력하도록 합니다.
noexpired = datetime.datetime.strptime(noexpired, '%Y-%m-%d %H:%M:%S') #마찬가지로 날짜타입으로 바꿔줍니다.

nowdate = urllib.request.urlopen('https://www.naver.com/').headers['Date'] #네이버의 날짜를 파싱해와서 현재시간을 저장합니다.
nowdate = int(time.mktime(time.strptime(nowdate, '%a, %d %b %Y %H:%M:%S %Z'))) #날짜를 시간화시켜줍니다.
nowdate = datetime.datetime.fromtimestamp(int(nowdate)).strftime('%Y-%m-%d %H:%M:%S') #만료날짜와 비교하기위해 같은 형식으로 변환시켜줍니다.
nowdate = datetime.datetime.strptime(nowdate, '%Y-%m-%d %H:%M:%S') #문자열 타입으로 되어있는 날짜를 날짜타입으로 변경해줍니다.
nowdate = nowdate + datetime.timedelta(hours=9) #그리니치 표준시로 되어있는 날짜를 9시간 더하여 한국 표준시로 바꾸어줍니다.

howlong = expried - nowdate #만료날짜와 현재날짜를 뺀값을 저장합니다.
days = howlong.days #만료날짜의 남은 일을 구합니다
hours = howlong.seconds // 3600 #만료날짜의 남은 시를 구합니다
minutes = howlong.seconds // 60 - hours * 60 #만료날짜의 남은 분을 구합니다.
seconds = howlong.seconds - hours * 3600 -minutes * 60 #만료날짜의  초를 구합니다.

if noexpired < expried: #만료날짜가 5555년보다 크면 무제한으로 출력합니다.
    print("무제한입니다.")
elif expried < nowdate: #만료날짜가 현재날짜보다 작으면 만료 출력
    print("만료되었습니다.")
elif expried > nowdate: #만료날짜가 현재날짜보다 크면 남은날짜 출력
    print("현재날짜: " + str(nowdate))
    print("만료날짜: " + str(expried))
    print('{}일 {}시간 {}분 {}초 남았습니다'.format(days,hours,minutes,seconds))
