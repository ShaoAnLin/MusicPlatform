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

# river bank
url = 'http://www.riverside.com.tw/index.php?option=com_cafe'
res = requests.get(url)

soup = BeautifulSoup(res.text, "html.parser")
data = soup.select('.concerts')

river_bank = []

ofile = open('out.txt', 'w')
idx = 0
for value in data[0].select('.show_name'):
	river_bank.append( Show(idx, value.text) )
	idx += 1

idx = 0
for value in data[0].select('.show_date'):
	river_bank[idx].set_date(value.select('.date')[0].text)
	river_bank[idx].set_year(value.select('.year')[0].text)
	idx += 1

idx = 0
for value in data[0].select('.price_wrapper'):
	river_bank[idx].set_price(value.select('.info')[0].text)
	river_bank[idx].set_drink(value.select('.info')[1].text)
	idx += 1

for show in river_bank:
	ofile.write('(%d)\nname: %s\ndate: %s\nyear: %s\n' % (show._idx + 1, show._name, show._date, show._year))
	ofile.write('price: %s\ndrink: %s\n\n' % (show._price, show._drink))
