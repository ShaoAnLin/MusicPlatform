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
	#ofile.write('%s\n' % value.text)

idx = 0
for value in data[0].select('.show_date'):
	river_bank[idx].set_date(value.select('.date')[0].text)
	idx += 1
	#ofile.write('%s\n' % value.select('.date')[0].text)

for show in river_bank:
	ofile.write('(%d) %s %s\n' % (show._idx + 1, show._name, show._date))
