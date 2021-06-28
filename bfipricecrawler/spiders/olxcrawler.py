from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from bfipricecrawler.items import CarItem
from bfipricecrawler.utils.utils import list_to_dict, clean_price, parse_location


class SpiderSpider(CrawlSpider):
    name = 'olx'
    start_urls = ['https://www.olx.co.id/mobil-bekas_c198']
    base_url = 'https://www.olx.co.id/'
    rules = [Rule(LinkExtractor(allow='item/'),
                  callback='parse_car', follow=True)]

    def parse_car(self, response):
        exists = response.xpath('//div[@class="_1f7-Z"]').extract_first()
        item = CarItem()
        if exists:
            try:
                deskripsi = response.xpath('/html/body/div/div/main/div/div/div/div[4]/section[1]/div/div/div[2]/p//text()').get()
                lokasi = parse_location(response.css('div[class="_2A3Wa"]  ::text').extract_first().split(','))
                data_deskripsi = list_to_dict(response.css('div[class="_3JPEe"] ::text').extract())
                item["url"] = response.url
                item['nama'] = response.css('h1[class="_3rJ6e"] ::text').extract_first()
                item['merek'] = data_deskripsi.get('Merek')
                item['model'] = data_deskripsi.get('Model')
                item['varian'] = data_deskripsi.get('Varian')
                item['transmisi'] = data_deskripsi.get('Transmisi')
                item["tahun"] = data_deskripsi.get('Tahun')
                item['provinsi'] = lokasi.get('provinsi')
                item['kabupaten_kecamatan'] = lokasi.get('kabupaten_kota')
                item['harga'] = int(clean_price(response.css('span[class="_2xKfz"] ::text').extract_first()))
                item['deskripsi'] = deskripsi
                item['lokasi'] = lokasi
                item['spesifikasi_ringkas'] = data_deskripsi
                item['sumber'] = 'Olx'
                yield item
            except Exception as e:
                print(str(e))
        else:
            print(response.url)

