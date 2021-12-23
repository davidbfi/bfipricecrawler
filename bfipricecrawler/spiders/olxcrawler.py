import re
from datetime import datetime
import pandas as pd
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
    start_urls = data[:100000]
    base_url = 'https://www.olx.co.id/'
    rules = [Rule(LinkExtractor(allow='item/'),
                  callback='parse_car', follow=True)]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'FileCrawled/Olx/olx5_{}.json'.format(int(datetime.now().strftime('%Y%m%d')))
    }

    def parse_car(self, response):
        failed_url = []
        exists = response.xpath('//div[@class="_31KwC"]').extract_first()
        item = CarItem()
        if exists:
            try:
                nama = response.css('div[class="_35xN1"] ::text').extract_first()
                try:
                    tahun = re.search(r"\(([A-Za-z0-9_]+)\)", nama).group(1) or ''
                except:
                    tahun = ""

                try:
                    varian_el = response.css('div[class="_3tLee"] ::text').extract_first().split(' ')
                except:
                    varian_el = response.css('div[class="_35xN1"] ::text').extract_first().split(' ')

                try:
                    alias_cc = float(varian_el[0])
                except:
                    alias_cc = 0

                parse_nama = nama.split(" ")
                merek = parse_nama[0].lower()
                model = ' '.join(parse_nama[1:-1]).capitalize()
                if model == 'Cr-V' or model == 'Hr-V' or model == 'Cr-v' or model == 'Hr-v' or model == 'Br-v':
                    new_model = model.upper()
                else:
                    new_model = model.capitalize()
                data = response.css('div[class="_1l939"] ::text').extract()
                data[-2] = "Cakupan mesin"
                data_deskripsi = list_to_dict(data)
                lokasi = olx_location(response.css('div[class="ZGU9S"] ::text').extract())
                deskripsi = olx_descriptiton(response.css('div[class="_2e_o8"] ::text').extract())

                try:
                    cakupan_mesin = int(float(varian_el[0]) * 1000)
                except Exception as e:
                    cakupan_mesin = data_deskripsi.get('Cakupan mesin')
                    cakupan_mesin = cakupan_mesin.split()[0]
                    cakupan_mesin = ''.join([n for n in cakupan_mesin if n.isdigit()])
                    cakupan_mesin = int(cakupan_mesin)

                try:
                    tanggal_update = response.css('div[class="_10dMT"] ::text').extract()[-1]
                    tanggal_update_ = pd.to_datetime(tanggal_update)
                    tanggal_diperbaharui = tanggal_update_
                    #tanggal_diperbaharui = tanggal_update_.strftime('%d %B %Y')
                except:
                    tanggal_diperbaharui = datetime.now()

                if lokasi.get('provinsi').strip() == 'Jakarta D.K.I.':
                    provinsi = "DKI Jakarta"
                elif lokasi.get('provinsi').strip() == 'Aceh D.I.':
                    provinsi = "Nangroe Aceh Darussalam"
                elif lokasi.get('provinsi').strip() == 'Yogyakarta D.I.':
                    provinsi = "Yogyakarta"
                else:
                    provinsi = lokasi.get('provinsi').strip()

                item["url"] = response.url
                item['nama'] = response.css('div[class="_35xN1"] ::text').extract_first()
                item['merek'] = merek or ""
                item['model'] = new_model or ""
                item['varian'] = ' '.join(varian_el[1:-1]).upper()
                item['transmisi'] = response.css('div[class="aOxkz"] ::text').extract()[-1]
                item['cakupan_mesin'] = cakupan_mesin
                item['alias_cc'] = alias_cc
                item["warna"] = ""
                item["tahun"] = tahun or ''
                item['provinsi'] = provinsi
                item['kabupaten_kecamatan'] = lokasi.get('kabupaten_kota').strip() or ''
                item['harga'] = int(price_parser(response.css('div[class="_3FkyT"] ::text').extract_first()))
                item['deskripsi'] = deskripsi
                item['lokasi'] = lokasi
                item['spesifikasi_ringkas'] = data_deskripsi
                item['sumber'] = 'Olx'
                item['tanggal_diperbaharui_sumber'] = tanggal_diperbaharui
                item['waktu_crawl'] = datetime.now().strftime('%d-%m-%Y')
                print(item['tanggal_diperbaharui_sumber'])
                yield item
            except Exception as e:
                failed_url.append(response.url)
                df = pd.DataFrame(failed_url, columns=["url"])
                df.to_csv('Failed/list_failed_olx7.csv', index=False)
                pass
        else:
            pass
            #print(response.url)


class SpiderSpider2(CrawlSpider):
    name = 'olx2'
    start_urls = data[100001:200000]
    base_url = 'https://www.olx.co.id/'
    rules = [Rule(LinkExtractor(allow='item/'),
                  callback='parse_car', follow=True)]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'FileCrawled/Olx/olx_6{}.json'.format(int(datetime.now().strftime('%Y%m%d')))
    }

    def parse_car(self, response):
        failed_url = []
        exists = response.xpath('//div[@class="_31KwC"]').extract_first()
        item = CarItem()
        if exists:
            try:
                nama = response.css('div[class="_35xN1"] ::text').extract_first()
                try:
                    tahun = re.search(r"\(([A-Za-z0-9_]+)\)", nama).group(1) or ''
                except:
                    tahun = ""

                try:
                    varian_el = response.css('div[class="_3tLee"] ::text').extract_first().split(' ')
                except:
                    varian_el = response.css('div[class="_35xN1"] ::text').extract_first().split(' ')

                try:
                    alias_cc = float(varian_el[0])
                except:
                    alias_cc = 0

                parse_nama = nama.split(" ")
                merek = parse_nama[0].lower()
                model = ' '.join(parse_nama[1:-1]).capitalize()
                if model == 'Cr-V' or model == 'Hr-V' or model == 'Cr-v' or model == 'Hr-v' or model == 'Br-v':
                    new_model = model.upper()
                else:
                    new_model = model.capitalize()
                data = response.css('div[class="_1l939"] ::text').extract()
                data[-2] = "Cakupan mesin"
                data_deskripsi = list_to_dict(data)
                lokasi = olx_location(response.css('div[class="ZGU9S"] ::text').extract())
                deskripsi = olx_descriptiton(response.css('div[class="_2e_o8"] ::text').extract())

                try:
                    cakupan_mesin = int(float(varian_el[0]) * 1000)
                except Exception as e:
                    cakupan_mesin = data_deskripsi.get('Cakupan mesin')
                    cakupan_mesin = cakupan_mesin.split()[0]
                    cakupan_mesin = ''.join([n for n in cakupan_mesin if n.isdigit()])
                    cakupan_mesin = int(cakupan_mesin)

                try:
                    tanggal_update = response.css('div[class="_10dMT"] ::text').extract()[-1]
                    tanggal_update_ = pd.to_datetime(tanggal_update)
                    tanggal_diperbaharui = tanggal_update_
                    # tanggal_diperbaharui = tanggal_update_.strftime('%d %B %Y')
                except:
                    tanggal_diperbaharui = datetime.now()

                if lokasi.get('provinsi').strip() == 'Jakarta D.K.I.':
                    provinsi = "DKI Jakarta"
                elif lokasi.get('provinsi').strip() == 'Aceh D.I.':
                    provinsi = "Nangroe Aceh Darussalam"
                elif lokasi.get('provinsi').strip() == 'Yogyakarta D.I.':
                    provinsi = "Yogyakarta"
                else:
                    provinsi = lokasi.get('provinsi').strip()

                item["url"] = response.url
                item['nama'] = response.css('div[class="_35xN1"] ::text').extract_first()
                item['merek'] = merek or ""
                item['model'] = new_model or ""
                item['varian'] = ' '.join(varian_el[1:-1]).upper()
                item['transmisi'] = response.css('div[class="aOxkz"] ::text').extract()[-1]
                item['cakupan_mesin'] = cakupan_mesin
                item['alias_cc'] = alias_cc
                item["warna"] = ""
                item["tahun"] = tahun or ''
                item['provinsi'] = provinsi
                item['kabupaten_kecamatan'] = lokasi.get('kabupaten_kota').strip() or ''
                item['harga'] = int(price_parser(response.css('div[class="_3FkyT"] ::text').extract_first()))
                item['deskripsi'] = deskripsi
                item['lokasi'] = lokasi
                item['spesifikasi_ringkas'] = data_deskripsi
                item['sumber'] = 'Olx'
                item['tanggal_diperbaharui_sumber'] = tanggal_diperbaharui
                item['waktu_crawl'] = datetime.now().strftime('%d-%m-%Y')
                print("ITEM", item['tanggal_diperbaharui_sumber'])
                yield item
            except Exception as e:
                failed_url.append(response.url)
                df = pd.DataFrame(failed_url, columns=["url"])
                df.to_csv('Failed/list_failed_olx7.csv', index=False)
                pass
        else:
            pass
            # print(response.url)


class SpiderSpider3(CrawlSpider):
    name = 'olx3'
    start_urls = data[200001:]
    base_url = 'https://www.olx.co.id/'
    rules = [Rule(LinkExtractor(allow='item/'),
                  callback='parse_car', follow=True)]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'FileCrawled/Olx/olx_7{}.json'.format(int(datetime.now().strftime('%Y%m%d')))
    }

    def parse_car(self, response):
        failed_url = []
        exists = response.xpath('//div[@class="_31KwC"]').extract_first()
        item = CarItem()
        if exists:
            try:
                nama = response.css('div[class="_35xN1"] ::text').extract_first()
                try:
                    tahun = re.search(r"\(([A-Za-z0-9_]+)\)", nama).group(1) or ''
                except:
                    tahun = ""

                try:
                    varian_el = response.css('div[class="_3tLee"] ::text').extract_first().split(' ')
                except:
                    varian_el = response.css('div[class="_35xN1"] ::text').extract_first().split(' ')

                try:
                    alias_cc = float(varian_el[0])
                except:
                    alias_cc = 0

                parse_nama = nama.split(" ")
                merek = parse_nama[0].lower()
                model = ' '.join(parse_nama[1:-1]).capitalize()
                if model == 'Cr-V' or model == 'Hr-V' or model == 'Cr-v' or model == 'Hr-v' or model == 'Br-v':
                    new_model = model.upper()
                else:
                    new_model = model.capitalize()
                data = response.css('div[class="_1l939"] ::text').extract()
                data[-2] = "Cakupan mesin"
                data_deskripsi = list_to_dict(data)
                lokasi = olx_location(response.css('div[class="ZGU9S"] ::text').extract())
                deskripsi = olx_descriptiton(response.css('div[class="_2e_o8"] ::text').extract())

                try:
                    cakupan_mesin = int(float(varian_el[0]) * 1000)
                except Exception as e:
                    cakupan_mesin = data_deskripsi.get('Cakupan mesin')
                    cakupan_mesin = cakupan_mesin.split()[0]
                    cakupan_mesin = ''.join([n for n in cakupan_mesin if n.isdigit()])
                    cakupan_mesin = int(cakupan_mesin)

                try:
                    tanggal_update = response.css('div[class="_10dMT"] ::text').extract()[-1]
                    tanggal_update_ = pd.to_datetime(tanggal_update)
                    tanggal_diperbaharui = tanggal_update_
                    # tanggal_diperbaharui = tanggal_update_.strftime('%d %B %Y')
                except:
                    tanggal_diperbaharui = datetime.now()

                if lokasi.get('provinsi').strip() == 'Jakarta D.K.I.':
                    provinsi = "DKI Jakarta"
                elif lokasi.get('provinsi').strip() == 'Aceh D.I.':
                    provinsi = "Nangroe Aceh Darussalam"
                elif lokasi.get('provinsi').strip() == 'Yogyakarta D.I.':
                    provinsi = "Yogyakarta"
                else:
                    provinsi = lokasi.get('provinsi').strip()

                item["url"] = response.url
                item['nama'] = response.css('div[class="_35xN1"] ::text').extract_first()
                item['merek'] = merek or ""
                item['model'] = new_model or ""
                item['varian'] = ' '.join(varian_el[1:-1]).upper()
                item['transmisi'] = response.css('div[class="aOxkz"] ::text').extract()[-1]
                item['cakupan_mesin'] = cakupan_mesin
                item['alias_cc'] = alias_cc
                item["warna"] = ""
                item["tahun"] = tahun or ''
                item['provinsi'] = provinsi
                item['kabupaten_kecamatan'] = lokasi.get('kabupaten_kota').strip() or ''
                item['harga'] = int(price_parser(response.css('div[class="_3FkyT"] ::text').extract_first()))
                item['deskripsi'] = deskripsi
                item['lokasi'] = lokasi
                item['spesifikasi_ringkas'] = data_deskripsi
                item['sumber'] = 'Olx'
                item['tanggal_diperbaharui_sumber'] = tanggal_diperbaharui
                item['waktu_crawl'] = datetime.now().strftime('%d-%m-%Y')
                print("ITEM", item['tanggal_diperbaharui_sumber'])
                yield item
            except Exception as e:
                failed_url.append(response.url)
                df = pd.DataFrame(failed_url, columns=["url"])
                df.to_csv('Failed/list_failed_olx7.csv', index=False)
                pass
        else:
            pass
            # print(response.url)

