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
    def set_year(self, year):
        self._year = year
    def set_price(self, price):
        self._price = price
    def set_drink(self, drink):
        self._drink = drink

def river_bank_crawler(show_list, url):
	res = requests.get(url)

	soup = BeautifulSoup(res.text, "html.parser")
	data = soup.select('.concerts')

	idx = 0
	for value in data[0].select('.show_name'):
		show_list.append( Show(idx, value.text) )
		idx += 1

	idx = 0
	for value in data[0].select('.show_date'):
		show_list[idx].set_date(value.select('.date')[0].text)
		show_list[idx].set_year(value.select('.year')[0].text)
		idx += 1

	idx = 0
	for value in data[0].select('.price_wrapper'):
		show_list[idx].set_price(value.select('.info')[0].text)
		show_list[idx].set_drink(value.select('.info')[1].text)
		idx += 1

	for show in show_list:
		ofile.write('(%d)\nname: %s\ndate: %s\nyear: %s\n' % (show._idx + 1, show._name, show._date, show._year))
		ofile.write('price: %s\ndrink: %s\n\n' % (show._price, show._drink))

ofile = open('out.txt', 'w')

river_bank_cafe_url = 'http://www.riverside.com.tw/index.php?option=com_cafe'
red_house_url = 'http://www.riverside.com.tw/index.php?option=com_livehouse'

red_house_list = []
river_bank_cafe_list = []

ofile.write('===== red house =====\n')
river_bank_crawler(red_house_list, red_house_url)

ofile.write('===== river bank cafe =====\n')
river_bank_crawler(river_bank_cafe_list, river_bank_cafe_url)
