# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BfipricecrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CarItem(scrapy.Item):
    nama = scrapy.Field()
    merek = scrapy.Field()
    model = scrapy.Field()
    varian = scrapy.Field()
    transmisi = scrapy.Field()
    lokasi = scrapy.Field()
    cakupan_mesin = scrapy.Field()
    alias_cc = scrapy.Field()
    provinsi = scrapy.Field()
    kabupaten_kecamatan = scrapy.Field()
    harga = scrapy.Field()
    url = scrapy.Field()
    tipe_penjual = scrapy.Field()
    sumber = scrapy.Field()
    warna = scrapy.Field()
    spesifikasi_ringkas = scrapy.Field()
    deskripsi = scrapy.Field()
    tanggal_diperbaharui_sumber = scrapy.Field()
    waktu_crawl = scrapy.Field()
    tahun = scrapy.Field()
    kelengkapan = scrapy.Field()
    spesifikasi_lengkap = scrapy.Field()


class SpesifikasiItem(scrapy.Item):
    pass


class CarOtr(scrapy.Item):
    model = scrapy.Field()
    tipe = scrapy.Field()
    harga_otr = scrapy.Field()
    sumber = scrapy.Field()

