from datetime import datetime
import re
import pandas as pd

import scrapy
from bfipricecrawler.items import CarItem
from bfipricecrawler.utils.utils import list_to_dict, price_parser, category_parser, date_parser, seller_parser, location_parser, tab_specifications_parser


def get_url():
    data = pd.read_csv('/home/david/Desktop/NOTEBOOK/NLP/mobil123/list_url_mobil123.csv')
    urls = data['urls']
    urls_ = []
    for url in urls:
        urls_.append(url)
    return urls_


data = get_url()


class Mobil123Crawler(scrapy.Spider):
    name = 'mobil123'
    start_urls = data
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'FileCrawled/Mobil123/mobil123_{}.json'.format(int(datetime.now().strftime('%Y%m%d')))
    }

    def parse(self, response):
        updated_date = date_parser(response.css('span[class="u-color-muted  u-text-7  u-hide@desktop  u-margin-bottom-xs  u-block"]  ::text').extract()[0].strip())
        category = category_parser(response.css('ul[class="c-breadcrumb  u-text-7"] ::text').extract())
        name = response.css('h1[class="listing__title  u-color-dark  u-margin-bottom-xs  u-text-3  u-text-4@mobile  u-text-bold"]  ::text').extract()[0].strip()
        try:
            cc = re.search('[0-9]+,[0-9]+', name.replace('.', ','))
            alias_cc = cc.group().replace(',', '.')
            alias_cc = int(float(alias_cc) * 1000)
        except:
            alias_cc = 0
        try:
            price = price_parser(response.css('h3[class="u-color-white  u-text-3  u-text-4@mobile  u-text-bold  u-margin-bottom-none  u-margin-top-xxs"] ::text').extract()[0])
            summary_specifications = list_to_dict(response.css('div[class="u-width-4/6  u-width-1@mobile"]  ::text').extract())
            location = location_parser(response.css(
                'span[class="c-chip  c-chip--sm  u-rounded  u-margin-right-xxs  c-chip--wrap "]  ::text').extract() + response.css(
                'span[class="c-chip  c-chip--sm  u-rounded  u-margin-right-xxs c-chip--wrap "]  ::text').extract() + response.css(
                'span[class="c-chip  c-chip--sm  u-rounded  u-margin-right-xxs c-chip--wrap "]  ::text').extract())
            seller_type = seller_parser(response.css('span[class="c-chip  c-chip--icon  u-rounded  c-chip--sm  u-margin-right-xxs  u-margin-bottom-xxs"] ::text').extract())
            specifications_tab = tab_specifications_parser(response.css('div[id="tab-specifications"] ::text').extract())
            equipments_tab = list_to_dict(response.css('div[id="tab-equipments"] ::text').extract())
            # seller = list_to_dict((response.css('div[id="tab-seller-notes"] ::text').extract()))
            try:
                cakupan_mesin = summary_specifications.get('Cakupan mesin')
                cakupan_mesin = int(cakupan_mesin.split()[0])
            except:
                cakupan_mesin = 0
            try:
                kabupaten_kecamatan = location.get('kabupaten_kota').strip()
            except:
                kabupaten_kecamatan = location.get('kecamatan').strip()


            item = CarItem()
            item["url"] = response.url
            item["nama"] = name
            item["merek"] = category.get('Merk') or ''
            item["model"] = category.get('Model') or ''
            item["varian"] = category.get('Variant').upper() or ''
            item["transmisi"] = summary_specifications.get('Transmisi') or ''
            item["warna"] = summary_specifications.get('Warna') or ''
            item["tahun"] = summary_specifications.get('Tahun Kendaraan') or ''
            item["harga"] = int(price) or ''
            item["cakupan_mesin"] = cakupan_mesin
            item['alias_cc'] = alias_cc
            item['provinsi'] = location.get('provinsi').strip() or ''
            item['kabupaten_kecamatan'] = kabupaten_kecamatan
            item['tipe_penjual'] = seller_type
            item['tanggal_diperbaharui_sumber'] = pd.to_datetime(updated_date)
            item['spesifikasi_ringkas'] = summary_specifications
            item['kelengkapan'] = equipments_tab
            item['spesifikasi_lengkap'] = specifications_tab
            item['sumber'] = "Mobil123"
            item['waktu_crawl'] = datetime.now().strftime('%d-%m-%Y')
            yield item

        except Exception as e:
            print("ERRROR", str(e) + response.url)





