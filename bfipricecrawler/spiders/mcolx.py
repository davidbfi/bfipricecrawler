import pandas as pd

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from bfipricecrawler.items import MotorItem
from bfipricecrawler.utils.utils import list_to_dict, price_parser,  olx_description_parser, olx_location


def get_url():
    data = pd.read_csv(r'/home/david/Downloads/csv/olx_motor.csv')
    urls = data['urls']
    urls_ = []
    for url in urls:
        urls_.append(url)
    return urls_


data = get_url()


class OlxCrawler(CrawlSpider):
    name = 'olxmotor'
    start_urls = data

    base_url = 'https://www.olx.co.id/'
    rules = [Rule(LinkExtractor(allow='item/'), callback='parse_motor', follow=True)]

    def parse_motor(self, response):
        exists = response.xpath('//div[@class="_3FF3q"]').extract_first()
        item = MotorItem()
        if exists:
            try:
                descriptions = olx_description_parser(
                  response.xpath('/html/body/div/div/main/div/div/div/div[4]/section[1]/div/div/div[2]//text()').getall())
                lokasi = olx_location(response.css('div[class="ZGU9S"] ::text').extract())
                summary_specifications = list_to_dict(response.css('div[class="_3JPEe"] ::text').extract())
                item["url"] = response.url
                item['nama'] = response.css('h1[class="_3rJ6e"] ::text').extract_first()
                item['merek'] = summary_specifications.get('Merek') or ""
                item['model'] = summary_specifications.get('Model') or ""
                item["tahun"] = summary_specifications.get('Tahun') or ""
                item['provinsi'] = lokasi.get('provinsi')
                item['kabupaten_kecamatan'] = lokasi.get('kabupaten_kota')
                item['harga_offline'] = int(price_parser(response.css('span[class="_2xKfz"] ::text').extract_first()))
                item['deskripsi'] = descriptions
                item['lokasi'] = lokasi
                item['spesifikasi_ringkas'] = summary_specifications
                item['sumber'] = 'Olx'
                yield item
                print(item)
            except Exception as e:
                print(str(e), response.url)
        else:
            print("false")