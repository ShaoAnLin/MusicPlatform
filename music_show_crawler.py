# -*- coding: utf8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests, json, io
from bs4 import BeautifulSoup

NAME = 'name'
DATE = 'date'
START_TIME = 'start_time'
END_TIME = 'end_time'
HREF = 'href'
IMG_HREF = 'img_href'
ARTISTS = 'artists'
ARTIST_NAME = 'artist_name'
ARTIST_HREF = 'artist_href'
PRICES = 'prices'
DRINK = 'drink'
LOCATION = 'location'

#======================= Functions =========================
def write_json(filename, show_list):
    with io.open(filename, 'w', encoding='utf8') as outfile:
        str_ = json.dumps(show_list,
                          indent=4, sort_keys=True,
                          separators=(',', ':'), ensure_ascii=False)
        outfile.write(str_)

def strip_tags(soup, invalid_tag, invalid_attribute):
    for tag in soup.findAll(True):
        if tag.name == invalid_tag:
            tag.replaceWith('')
    return soup

# TODO: show time can only be obtained by clicking "More Info."
def river_bank_crawler(show_list, url):
    res = requests.get(url)
    res.encoding = 'utf8'
    soup = BeautifulSoup(res.text, 'html.parser')
    data = soup.select('.concerts')

    for show_info in data[0].select('.show_info'):
        show_detail = {}
        show_name = show_info.select('.show_name')[0]
        show_detail[NAME] = show_name.text

        show_date = show_info.select('.show_date')[0]
        show_date_text = strip_tags(show_date.select('.date')[0], 'span', 'date_slash').text
        show_year_date = show_date.select('.year')[0].text + show_date_text
        show_detail[DATE] = show_year_date
        # TODO: convert to YYYY-MM-DD

        price_wrapper = show_info.select('.price_wrapper')[0]
        show_detail[PRICES] = price_wrapper.select('.info')[0].text
        show_detail[DRINK] = price_wrapper.select('.info')[1].text

        show_photo = show_info.select('.show_photo')[0]
        show_detail[IMG_HREF] = riverside_homepage + show_photo.find("img")['src']
        show_list.append(show_detail)

def witch_house_crawler(show_list, url):
    res = requests.get(url)
    res.encoding = 'utf8'
    soup = BeautifulSoup(res.text, "html.parser")
    data = soup.select('.event-group')

    for show_info in data[0].select('.event-box'):
        show_detail = {}
        event_name = show_info.select('.event-name')[0]
        show_detail[NAME] = event_name.text

        event_date_list = show_info.select('.date')
        event_date = '%s-%s' % (event_date_list[0].text, event_date_list[2].text)
        show_detail[DATE] = event_date
        # TODO: convert to YYYY-MM-DD

        event_time_list = show_info.select('.time')
        show_detail[START_TIME] = event_time_list[0].text
        show_detail[END_TIME] = event_time_list[1].text
        # TODO: convert to HH:MM

        event_img = show_info.select('.event-img')[0]
        show_detail[IMG_HREF] = event_img.find("img")['src']
        show_list.append(show_detail)

#======================= Main =========================
ofile = open('out.txt', 'w')

riverside_homepage = 'http://www.riverside.com.tw/'
river_bank_cafe_url = riverside_homepage + 'index.php?option=com_cafe'
red_house_url = riverside_homepage + 'index.php?option=com_livehouse'
witch_house_url = 'http://www.witchhouse.org/#event'

red_house_list = []
river_bank_cafe_list = []
witch_house_list = []

river_bank_crawler(red_house_list, red_house_url)
river_bank_crawler(river_bank_cafe_list, river_bank_cafe_url)
witch_house_crawler(witch_house_list, witch_house_url)

write_json('red_house.json', red_house_list)
write_json('river_bank_cafe.json', river_bank_cafe_list)
write_json('witch_house.json', witch_house_list)