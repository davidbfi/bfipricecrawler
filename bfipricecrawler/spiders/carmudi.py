import re
from datetime import datetime
import pandas as pd

import scrapy
from scrapy import Request

from bfipricecrawler.items import CarItem
from bfipricecrawler.utils.utils import list_to_dict, price_parser, location_parser, date_parser, category_parser, \
    seller_parser, tab_specifications_parser, tab_equipments_parser


def get_url():
    data = pd.read_csv('/home/david/Desktop/NOTEBOOK/NLP/list_url_carmudi.csv')
    urls = data['urls']
    urls_ = []
    for url in urls:
        urls_.append(url)
    return urls_


data = get_url()


class CarmudiCrawler(scrapy.Spider):
    name = 'carmudi'
    urls = data
    start_urls = data[:100]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': './carmudi_{}.json'.format(int(datetime.now().strftime('%Y%m%d')))
        }

    def parse(self, response):
        updated_date = date_parser(response.css(
            'span[class="u-color-muted  u-text-7  u-hide@desktop  u-margin-bottom-xs  u-block"]  ::text').extract()[
                                       0].strip())
        category = category_parser(response.css('ul[class="c-breadcrumb  u-text-7"] ::text').extract())
        name = response.css(
            'h1[class="listing__title  u-color-dark  u-margin-bottom-xs  u-text-3  u-text-4@mobile  u-text-bold"]  ::text').extract()[
            0].strip()
        try:
            cc = re.search('[0-9]+,[0-9]+', name.replace('.', ','))
            alias_cc = cc.group().replace(',', '.')
        except:
            alias_cc = ''
        price = price_parser(response.css('div[class="listing__item-price"] ::text').extract()[1])
        summary_specifications = list_to_dict(
            response.css('div[class="u-width-4/6  u-width-1@mobile"]  ::text').extract())
        location = location_parser(response.css(
            'span[class="c-chip  c-chip--sm  u-rounded  u-margin-right-xxs  c-chip--wrap "]  ::text').extract() + response.css(
            'span[class="c-chip  c-chip--sm  u-rounded  u-margin-right-xxs c-chip--wrap "]  ::text').extract())
        seller_type = seller_parser(response.css(
            'span[class="c-chip  c-chip--icon  u-rounded  c-chip--sm  u-margin-right-xxs  u-margin-bottom-xxs"] ::text').extract())
        specifications_tab = tab_specifications_parser(response.css('div[id="tab-specifications"] ::text').extract())
        equipments_tab = tab_equipments_parser(response.css('div[id="tab-equipments"] ::text').extract())
        # seller = list_to_dict((response.css('div[id="tab-seller-notes"] ::text').extract())) TODO

        item = CarItem()
        item["url"] = response.url
        item["nama"] = name
        item["merek"] = category.get('Merk') or ''
        item["model"] = category.get('Model') or ''
        item["varian"] = category.get('Variant') or ''
        item["transmisi"] = summary_specifications.get('Transmisi') or ''
        item["warna"] = summary_specifications.get('Warna') or ''
        item["tahun"] = summary_specifications.get('Tahun Kendaraan') or ''
        item["harga"] = int(price) or ''
        item['alias_cc'] = alias_cc
        item['provinsi'] = location.get('provinsi').strip() or ''
        item['kabupaten_kecamatan'] = location.get('kabupaten_kota').strip()
        item['tipe_penjual'] = seller_type
        item['tanggal_diperbaharui_sumber'] = updated_date.strip()
        item['spesifikasi_ringkas'] = summary_specifications
        item['kelengkapan'] = equipments_tab
        item['spesifikasi_lengkap'] = specifications_tab
        item['sumber'] = "Carmudi"
        yield item
