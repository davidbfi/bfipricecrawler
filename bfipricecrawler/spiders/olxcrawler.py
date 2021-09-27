import re
from datetime import datetime
import pandas as pd
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from bfipricecrawler.items import CarItem
from bfipricecrawler.utils.utils import list_to_dict, price_parser, olx_location, olx_descriptiton


def get_url():
    data = pd.read_csv('/home/david/Desktop/NOTEBOOK/NLP/list_one_olx.csv')
    urls = data['urls']
    urls_ = []
    for url in urls:
        urls_.append(url)
    return urls_


data = get_url()


class SpiderSpider(CrawlSpider):
    name = 'olx'
    start_urls = data[:1]
    base_url = 'https://www.olx.co.id/'
    rules = [Rule(LinkExtractor(allow='item/'),
                  callback='parse_car', follow=True)]

    # custom_settings = {
    #     'FEED_FORMAT': 'json',
    #     'FEED_URI': 'FileCrawled/Olx/olx_{}.json'.format(int(datetime.now().strftime('%Y%m%d')))
    # }

    def parse_car(self, response):
        exists = response.xpath('//div[@class="_31KwC"]').extract_first()
        item = CarItem()
        if exists:
            try:
                nama = response.css('div[class="_35xN1"] ::text').extract_first()
                try:
                    tahun = re.search(r"\(([A-Za-z0-9_]+)\)", nama).group(1) or ''
                except:
                    tahun = ''
                parse_nama = nama.split(" ")
                merek = parse_nama[0]
                model = ' '.join(parse_nama[1:-1])
                data = response.css('div[class="_1l939"] ::text').extract()
                data[-2] = "Cakupan mesin"
                data_deskripsi = list_to_dict(data)
                lokasi = olx_location(response.css('div[class="ZGU9S"] ::text').extract())
                deskripsi = olx_descriptiton(response.css('div[class="_2e_o8"] ::text').extract())
                varian_el = response.css('div[class="_3tLee"] ::text').extract_first().split(' ')
                item["url"] = response.url
                item['nama'] = response.css('div[class="_35xN1"] ::text').extract_first()
                item['merek'] = merek
                item['model'] = model or ""
                item['varian'] = ' '.join(varian_el[1:-1])
                item['transmisi'] = response.css('div[class="aOxkz"] ::text').extract()[-1]
                item['alias_cc'] = varian_el[0]
                item["warna"] = ""
                item["tahun"] = tahun or ''
                item['provinsi'] = lokasi.get('provinsi').strip() or ' '
                item['kabupaten_kecamatan'] = lokasi.get('kabupaten_kota').strip() or ''
                item['harga'] = int(price_parser(response.css('div[class="_3FkyT"] ::text').extract_first()))
                item['deskripsi'] = deskripsi
                item['lokasi'] = lokasi
                item['spesifikasi_ringkas'] = data_deskripsi
                item['sumber'] = 'Olx'
                item['tanggal_diperbaharui_sumber'] = response.css('div[class="_10dMT"] ::text').extract()[-1]
                item['waktu_crawl'] = datetime.now().strftime('%d-%m-%Y')
                yield item
            except Exception as e:
                pass
        else:
            print(response.url)

