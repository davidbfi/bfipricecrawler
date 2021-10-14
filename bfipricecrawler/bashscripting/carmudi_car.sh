#!/bin/sh
cd /var/www/bfipricecrawler
source bfipricecrawler/bin/activate
scrapy crawl carmudi --nolog