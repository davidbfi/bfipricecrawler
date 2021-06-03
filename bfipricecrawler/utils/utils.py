import re
import requests
import itertools
from lxml.html import fromstring


class ExpectedConditionModifier:
    """ Use with WebDriverWait to combine expected_conditions
        in an OR.
    """
    def __init__(self, *args):
        self.ecs = args

    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver):
                    return True
            except:
                pass


def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies


def clean_date():
    pass


def get_location():
    pass


def tipe_penjual():
    pass


def list_to_dict(_list):
    ringkasan_spesifikasi_new = []
    for line in _list:
        if not line.strip() == "":
            ringkasan_spesifikasi_new.append(line)
    if len(ringkasan_spesifikasi_new) == int(23):
        ringkasan_spesifikasi_new = ringkasan_spesifikasi_new[0:6] + ringkasan_spesifikasi_new[9:23]

    return dict(itertools.zip_longest(*[iter(ringkasan_spesifikasi_new)] * 2, fillvalue=""))


def clean_price(price):
    if '-' in price:
        splitted_price = price.split('-')[0]
        cleaned_price = re.sub('[^0-9]', '', splitted_price)
    else:
        cleaned_price = re.sub('[^0-9]', '', price)
    return cleaned_price


def parse_location(lokasi):
    tingkatan_wilayah = ['kecamatan', 'kabupaten_kota', 'provinsi']
    return dict(zip(tingkatan_wilayah, lokasi))
