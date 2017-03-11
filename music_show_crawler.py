# -*- coding: utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
from bs4 import BeautifulSoup

class Show:
    def __init__(self, idx, name):
    	self._idx = idx
        self._name = name
    def set_date(self, date):
        self._date = date
    def set_time(self, time):
    	self._time = time
    def set_year(self, year):
        self._year = year
    def set_price(self, price):
        self._price = price
    def set_drink(self, drink):
        self._drink = drink
    def set_image_url(self, imgUrl):
    	self._imageUrl = imgUrl

#======================= Functions =========================
# TODO: show time can only be obtained by clicking "More Info."
def river_bank_crawler(show_list, url):
	res = requests.get(url)
	res.encoding = 'utf8'
	soup = BeautifulSoup(res.text, "html.parser")
	data = soup.select('.concerts')

	idx = 0
	for show_info in data[0].select('.show_info'):
		show_name = show_info.select('.show_name')[0]
		show_list.append( Show(idx, show_name.text) )

		show_date = show_info.select('.show_date')[0]
		show_list[idx].set_date(show_date.select('.date')[0].text)
		show_list[idx].set_year(show_date.select('.year')[0].text)

		price_wrapper = show_info.select('.price_wrapper')[0]
		show_list[idx].set_price(price_wrapper.select('.info')[0].text)
		show_list[idx].set_drink(price_wrapper.select('.info')[1].text)

		show_photo = show_info.select('.show_photo')[0]
		show_list[idx].set_image_url(riverside_homepage + show_photo.find("img")['src'])
		idx += 1

	for show in show_list:
		ofile.write('(%d)\nname: %s\ndate: %s\nyear: %s\n' % (show._idx + 1, show._name, show._date, show._year))
		ofile.write('price: %s\ndrink: %s\n' % (show._price, show._drink))
		ofile.write('image_url: %s\n\n' % show._imageUrl)

def witch_house_crawler(show_list, url):
	res = requests.get(url)
	res.encoding = 'utf8'
	soup = BeautifulSoup(res.text, "html.parser")
	data = soup.select('.event-group')

	idx = 0
	for show_info in data[0].select('.event-title-group'):
		event_name = show_info.select('.event-name')[0]
		show_list.append( Show(idx, event_name.text) )

		event_date_list = show_info.select('.date')
		event_weekday = show_info.select('.weekday')[0]
		event_date = '%s/%s(%s)' % (event_date_list[0].text, event_date_list[2].text, event_weekday.text)
		show_list[idx].set_date(event_date)

		event_time_list = show_info.select('.time')
		event_time = '%s-%s' % (event_time_list[0].text, event_time_list[1].text)
		show_list[idx].set_time(event_time)
		idx += 1

		event_img = show_info.select('.event-img')[0]
		show_list[idx].set_image_url(value.find("img")['src'])
		idx += 1

	for show in show_list:
		ofile.write('(%d)\nname: %s\ndate: %s\ntime: %s\n' % (show._idx + 1, show._name, show._date, show._time))
		ofile.write('image_url: %s\n\n' % show._imageUrl)

#======================= Main =========================
ofile = open('out.txt', 'w')

riverside_homepage = 'http://www.riverside.com.tw/'
river_bank_cafe_url = riverside_homepage + 'index.php?option=com_cafe'
red_house_url = riverside_homepage + 'index.php?option=com_livehouse'
witch_house_url = 'http://www.witchhouse.org/#event'

red_house_list = []
river_bank_cafe_list = []
witch_house_list = []

#ofile.write('===== red house =====\n')
#river_bank_crawler(red_house_list, red_house_url)

ofile.write('===== river bank cafe =====\n')
river_bank_crawler(river_bank_cafe_list, river_bank_cafe_url)

#ofile.write('===== witch house =====\n')
#witch_house_crawler(witch_house_list, witch_house_url)
