import json
import requests
import itertools
import pandas as pd
from bs4 import BeautifulSoup

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from scrapy_selenium import SeleniumRequest

from bfipricecrawler.utils.utils import ExpectedConditionModifier
from bfipricecrawler.items import CarItem
from bfipricecrawler.utils.utils import list_to_dict, clean_price


def get_url():
    data = pd.read_csv('/home/david/Desktop/NOTEBOOK/NLP/list_url_carmudi.csv')
    urls = data['urls']
    return urls


data = get_url()


class CarmudiCrawler(scrapy.Spider):
    name = 'carmudi'
    urls = data
    start_urls = urls

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse,
                wait_time=1,
                wait_until=ExpectedConditionModifier(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "listing__price  delta  weight--bold")),
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "listing__section__head"))
                )
            )

    def parse(self, response):
        item = CarItem()
        item["url"] = response.url
        tabel_spesifikasi_ringkas = response.css('div[class="listing__key-listing__list"] ::text').extract()
        spesifikasi_ringkas = list_to_dict(tabel_spesifikasi_ringkas)
        informasi_penjual = response.css('div[class="list-item  soft-half--ends"] ::text').extract()
        update_date = response.css('div[class="listing__updated  visuallyhidden--palm"] ::text').extract_first().split(':')[-1]
        item["nama"] = response.css('h1[class="headline  listing__title  delta  flush--bottom"] ::text').extract_first()
        item["merek"] = spesifikasi_ringkas.get('Merek')
        item["model"] = spesifikasi_ringkas.get('Model')
        item["varian"] = spesifikasi_ringkas.get('Varian')
        item["transmisi"] = spesifikasi_ringkas.get('Transmisi')
        item["harga"] = int(clean_price(response.css('div[class="listing__price  delta  weight--bold"] ::text').extract_first()))
        item['provinsi'] = informasi_penjual[-1].split('»')[0].strip()
        item['kabupaten_kecamatan'] = informasi_penjual[-1].split('»')[-1].strip()
        item['tipe_penjual'] = informasi_penjual[1].strip()
        item['tanggal_diperbaharui_sumber'] = update_date.strip()
        item['spesifikasi_ringkas'] = spesifikasi_ringkas
        item['sumber'] = "Carmudi"
        yield item
