import requests
import re

from bs4 import BeautifulSoup
from decouple import config

aed_target_url = config('AED_TARGET_URL')
usd_target_url = config('USD_TARGET_URL')
usd_remittance_target_url = config('USD_REMITTANCE_TARGET_URL')
eu_target_url = config('EU_TARGET_URL')
eu_remittance_target_url = config('EU_REMITTANCE_TARGET_URL')
pound_target_url = config('POUND_TARGET_URL')
cad_target_url = config('CAD_TARGET_URL')
cny_target_url = config('CNY_TARGET_URL')
aud_target_url = config('AUD_TARGET_URL')


def get_parser(target_url):
    return BeautifulSoup(requests.get(target_url).text, 'html.parser')


def get_bs_table(target_url):
    return get_parser(target_url).find('table', {"class": "arz-table"})


def parse_table(bs_table):
    data = []
    rows = bs_table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values

    return data


def buy_price(target_url):
    data = parse_table(get_bs_table(target_url))
    return sanitize(data[0][1])


def sell_price(target_url):
    data = parse_table(get_bs_table(target_url))
    return sanitize(data[1][1])

def sanitize(text):
    return re.sub("[^0-9,]", "", text)