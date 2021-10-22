import re
from datetime import datetime
import pandas as pd
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from bfipricecrawler.items import CarItem
from bfipricecrawler.utils.utils import list_to_dict, price_parser, olx_location, olx_descriptiton


def get_url():
    data = pd.read_csv('/home/david/Desktop/NOTEBOOK/NLP/olx/list_url_olx.csv')
    urls = data['urls']
    urls_ = []
    for url in urls:
        urls_.append(url)
    return urls_


data = get_url()


class SpiderSpider(CrawlSpider):
    name = 'olx'
    start_urls = data
    base_url = 'https://www.olx.co.id/'
    rules = [Rule(LinkExtractor(allow='item/'),
                  callback='parse_car', follow=True)]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'FileCrawled/Olx/olx_{}.json'.format(int(datetime.now().strftime('%Y%m%d')))
    }

    def parse_car(self, response):
        exists = response.xpath('//div[@class="_31KwC"]').extract_first()
        item = CarItem()
        if exists:
            try:
                nama = response.css('div[class="_35xN1"] ::text').extract_first()
                try:
                    tahun = re.search(r"\(([A-Za-z0-9_]+)\)", nama).group(1) or ''
                except:
                    tahun = ""

                parse_nama = nama.split(" ")
                merek = parse_nama[0]
                model = ' '.join(parse_nama[1:-1]).capitalize()
                data = response.css('div[class="_1l939"] ::text').extract()
                data[-2] = "Cakupan mesin"
                data_deskripsi = list_to_dict(data)
                lokasi = olx_location(response.css('div[class="ZGU9S"] ::text').extract())
                deskripsi = olx_descriptiton(response.css('div[class="_2e_o8"] ::text').extract())

                try:
                    cakupan_mesin = data_deskripsi.get('Cakupan mesin')
                    cakupan_mesin = cakupan_mesin.split()[0]
                    cakupan_mesin = ''.join([n for n in cakupan_mesin if n.isdigit()])
                    cakupan_mesin = int(cakupan_mesin)
                except Exception as e:
                    cakupan_mesin = 0

                try:
                    tanggal_update = response.css('div[class="_10dMT"] ::text').extract()[-1]
                    tanggal_update = datetime.strptime(tanggal_update, '%d/%M/%y')
                    tanggal_update = tanggal_update.strftime('%d %B %Y')
                except:
                    tanggal_update = ""
                try:
                    varian_el = response.css('div[class="_3tLee"] ::text').extract_first().split(' ')
                except:
                    varian_el = response.css('div[class="_35xN1"] ::text').extract_first().split(' ')

                try:
                    alias_cc = float(varian_el[0])
                except:
                    alias_cc = 0
                item["url"] = response.url
                item['nama'] = response.css('div[class="_35xN1"] ::text').extract_first()
                item['merek'] = merek.capitalize() or ""
                item['model'] = model.capitalize() or ""
                item['varian'] = ' '.join(varian_el[1:-1]).upper()
                item['transmisi'] = response.css('div[class="aOxkz"] ::text').extract()[-1]
                item['cakupan_mesin'] = cakupan_mesin
                item['alias_cc'] = alias_cc
                item["warna"] = ""
                item["tahun"] = tahun or ''
                item['provinsi'] = lokasi.get('provinsi').strip() or ' '
                item['kabupaten_kecamatan'] = lokasi.get('kabupaten_kota').strip() or ''
                item['harga'] = int(price_parser(response.css('div[class="_3FkyT"] ::text').extract_first()))
                item['deskripsi'] = deskripsi
                item['lokasi'] = lokasi
                item['spesifikasi_ringkas'] = data_deskripsi
                item['sumber'] = 'Olx'
                item['tanggal_diperbaharui_sumber'] = tanggal_update
                item['waktu_crawl'] = datetime.now().strftime('%d-%m-%Y')
                #print("ITEM", item)
                yield item
            except Exception as e:
                print("STR", str(e), response.url)
                pass
        else:
            pass
            #print(response.url)

