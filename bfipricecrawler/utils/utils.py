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


def date_parser(eldate):
    return eldate.split(':')[1]


def seller_parser(elseller):
    values = set()
    for line in elseller:
        if not line.strip() == "":
            values.add(line.strip())
    return list(values)[0]


def list_to_dict(_list):
    print(_list)
    ringkasan_spesifikasi_new = []
    for line in _list:
        if not line.strip() == "":
            ringkasan_spesifikasi_new.append(line)

    if len(ringkasan_spesifikasi_new) == 21:
        ringkasan_spesifikasi_new = ringkasan_spesifikasi_new[0:6] + ringkasan_spesifikasi_new[9:21]
    if len(ringkasan_spesifikasi_new) == int(23):
        ringkasan_spesifikasi_new = ringkasan_spesifikasi_new[0:6] + ringkasan_spesifikasi_new[9:23]
    if len(ringkasan_spesifikasi_new) == int(25):
        ringkasan_spesifikasi_new = ringkasan_spesifikasi_new[2:8] + ringkasan_spesifikasi_new[11:]
    return dict(itertools.zip_longest(*[iter(ringkasan_spesifikasi_new)] * 2, fillvalue=""))


def price_parser(elprice):
    if '-' in elprice:
        splitted_price = elprice.split('-')[0]
        cleaned_price = re.sub('[^0-9]', '', splitted_price)
    else:
        cleaned_price = re.sub('[^0-9]', '', elprice)
    return cleaned_price


def location_parser(ellocation):
    keys = ['kecamatan', 'kabupaten_kota', 'provinsi']
    values = set()
    for line in ellocation:
        if not line.strip() == "":
            values.add(line.strip())

    return dict(zip(keys, list(values)))


def category_parser(elbreadcum):
    keys = ['Type', 'Merk', 'Model', 'Variant']

    values = []
    for line in elbreadcum:
        if not line.strip() == "":
            values.append(line)

    category_dict = dict(zip(keys, values[1:] + ['']*(len(keys)-len(values[1:]))))

    return category_dict


def tab_specifications_parser(elspecifications):
    specification = []
    for line in elspecifications:
        if not (line.strip() == "" or line.strip() == 'General' or line.strip() == 'Spesifikasi Mesin' or
                line.strip() == 'Dimensi dan Berat' or line.strip() == 'Dimensi dan Berat' or line.strip() == 'Kinerja & Ekonomi' or line.strip() == 'Setir'):
            specification.append(line)

    return dict(itertools.zip_longest(*[iter(specification[1:])] * 2, fillvalue=""))


def tab_equipments_parser(elequipments):
    equipments = []
    for line in elequipments:
        if not (line.strip() == "" or line.strip() == 'Comfort' or line.strip() == 'Convenience' or
                line.strip() == 'Keamanan' or line.strip() == 'Lighting' or line.strip() == 'Entertainment'):
            equipments.append(line)

    return dict(itertools.zip_longest(*[iter(equipments)] * 2, fillvalue=""))


def olx_descriptiton(eldescription):
    description = eldescription[1:]
    return ' '.join(description)


def olx_varian(elvarian):
    return


def olx_location(location):
    keys = ["kecamatan", "kabupaten_kota", "provinsi"]
    values = location[0].split(',')
    return dict(zip(keys, list(values)))

