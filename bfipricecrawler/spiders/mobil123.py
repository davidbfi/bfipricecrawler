import json
import requests
import itertools
import pandas as pd

import scrapy
from scrapy import Request
from bfipricecrawler.utils.utils import ExpectedConditionModifier
from bfipricecrawler.items import CarItem
from bfipricecrawler.utils.utils import list_to_dict, price_parser, category_parser, date_parser, seller_parser, location_parser, tab_specifications_parser


def get_url():
    data = pd.read_csv('/home/david/Desktop/NOTEBOOK/NLP/list_url_mobil123.csv')
    urls = data['urls']
    urls_ = []
    for url in urls:
        urls_.append(url)
    return urls_


data = get_url()


class Mobil123Crawler(scrapy.Spider):
    name = 'mobil123'
    start_urls = data[200:210]

    def parse(self, response):
        links = response.xpath('/html/body/main/article/section/section[2]/section[1]/div/div/div[1]/div[1]/div/div[1]/div/a[2]/@href').extract()
        for link in links:
            yield Request(response.url + link, callback=self.parse_kelengkapan)

    def parse_kelengkapan(self, response):
        updated_date = date_parser(response.css('span[class="u-color-muted  u-text-7  u-hide@desktop  u-margin-bottom-xs  u-block"]  ::text').extract()[0].strip())
        category = category_parser(response.css('ul[class="c-breadcrumb  u-text-7"] ::text').extract())
        name = response.css('h1[class="listing__title  u-color-dark  u-margin-bottom-xs  u-text-3  u-text-4@mobile  u-text-bold"]  ::text').extract()[0].strip()
        price = price_parser(response.css('div[class="listing__item-price"] ::text').extract()[1])
        summary_spesifications = list_to_dict(response.css('div[class="u-width-4/6  u-width-1@mobile"]  ::text').extract())
        location = location_parser(response.css('span[class="c-chip  c-chip--sm  u-rounded  u-margin-right-xxs  c-chip--wrap "]  ::text').extract() + response.css('span[class="c-chip  c-chip--sm  u-rounded  u-margin-right-xxs c-chip--wrap "]  ::text').extract())
        seller_type = seller_parser(response.css('span[class="c-chip  c-chip--icon  u-rounded  c-chip--sm  u-margin-right-xxs  u-margin-bottom-xxs"] ::text').extract())
        # spesifications_tab = tab_specifications_parser(response.css('div[id="tab-specifications"] ::text').extract())
        # equipments_tab = list_to_dict(response.css('div[id="tab-equipments"] ::text').extract())
        # seller = list_to_dict((response.css('div[id="tab-seller-notes"] ::text').extract()))
        item = CarItem()
        item["url"] = response.url
        item["nama"] = name
        item["merek"] = category.get('Merk') or ''
        item["model"] = category.get('Model') or ''
        item["varian"] = category.get('Variant') or ''
        item["transmisi"] = summary_spesifications.get('Transmisi') or ''
        item["warna"] = summary_spesifications.get('Warna') or ''
        item["tahun"] = summary_spesifications.get('Tahun') or ''
        item["harga"] = int(price) or ''
        item['provinsi'] = location.get('provinsi').strip()
        item['kabupaten_kecamatan'] = location.get('kabupaten_kota').strip()
        item['tipe_penjual'] = seller_type
        item['tanggal_diperbaharui_sumber'] = updated_date.strip()
        item['spesifikasi_ringkas'] = summary_spesifications
        item['sumber'] = "Mobil123"




