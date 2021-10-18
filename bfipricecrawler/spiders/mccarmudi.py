import scrapy
import pandas as pd

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from bfipricecrawler.items import CarItem, MotorItem
from bfipricecrawler.utils.utils import list_to_dict, price_parser, location_parser, \
date_parser, category_parser, seller_parser, tab_specifications_parser, tab_equipments_parser, carmudi_url_parser


def get_url():
    data = pd.read_csv('/home/david/Downloads/csv/carmudi_motor.csv')
    urls = data['urls']
    urls_ = []
    for url in urls:
        urls_.append(url)
    return urls_


data = get_url()


class CarmudiCrawler(scrapy.Spider):
    name = 'mccarmudi'
    start_urls = data

    base_url = 'https://www.carmudi.co.id/'
    allowed_link = [
        'dijual/',
        'motor-baru-dijual/',
        'motor-bekas-dijual/',
        'motor-dijual/'
    ]

    def parse(self, response):
        links = carmudi_url_parser(response.css(
            'article[class="listing  listing--card    box  relative  push--top  palm-hard  js--listing  js--multi-lead"] a::attr(href)').extract())
        for link in links:
            yield Request(link, callback=self.parse_motor)

    def parse_motor(self, response):
        try:
            updated_date = date_parser(response.css(
                'span[class="u-color-muted  u-text-7  u-hide@desktop  u-margin-bottom-xs  u-block"]  ::text').extract()[
                                           0].strip())
            category = category_parser(response.css('ul[class="c-breadcrumb  u-text-7"] ::text').extract())
            name = response.css(
                'h1[class="listing__title  u-color-dark  u-margin-bottom-xs  u-text-3  u-text-4@mobile  u-text-bold"]  ::text').extract()[
                0].strip()
            price = price_parser(response.css('div[class="listing__item-price"] ::text').extract()[1])
            summary_specifications = list_to_dict(
                response.css('div[class="u-width-4/6  u-width-1@mobile"]  ::text').extract())
            location = location_parser(response.css(
                'span[class="c-chip  c-chip--sm  u-rounded  u-margin-right-xxs  u-margin-bottom-xxs"]  ::text').extract() + response.css(
                'span[class="c-chip  c-chip--sm  u-rounded  u-margin-right-xxs  u-margin-bottom-xxs"]  ::text').extract() + response.css(
                'span[class="c-chip  c-chip--sm  u-rounded  u-margin-right-xxs  u-margin-bottom-xxs"]  ::text').extract())
            seller_type = seller_parser(response.css(
                'span[class="c-chip  c-chip--icon  u-rounded  c-chip--sm  u-margin-right-xxs  u-margin-bottom-xxs"] ::text').extract())
            specifications_tab = tab_specifications_parser(
                response.css('div[id="tab-specifications"] ::text').extract())
            equipments_tab = tab_equipments_parser(response.css('div[id="tab-equipments"] ::text').extract())

            item = MotorItem()

            item["url"] = response.url
            item["nama"] = name
            item["merek"] = category.get('Merk') or ''
            item["model"] = category.get('Model') or ''
            item["varian"] = category.get('Variant') or ''
            item["transmisi"] = summary_specifications.get('Transmisi') or ''
            item["tahun"] = summary_specifications.get('Tahun Kendaraan') or ''
            item["harga_offline"] = int(price) or ''
            item['provinsi'] = location.get('provinsi') or ''
            item['kabupaten_kecamatan'] = location.get('kabupaten_kota') or ''
            item['tipe_penjual'] = seller_type
            item['tanggal_diperbaharui_sumber'] = updated_date.strip()
            item['spesifikasi_ringkas'] = summary_specifications
            item['kelengkapan'] = equipments_tab
            item['spesifikasi_lengkap'] = specifications_tab
            item['sumber'] = "Carmudi"
            yield item
        except Exception as e:
            print(str(e))
