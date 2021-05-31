from shutil import which

BOT_NAME = 'bfipricecrawler'

SPIDER_MODULES = ['bfipricecrawler.spiders']
NEWSPIDER_MODULE = 'bfipricecrawler.spiders'

DOWNLOAD_TIMEOUT = 540

# DOWNLOAD_DELAY = 5

DEPTH_LIMIT = 10

EXTENSIONS = {
    'scrapy.extensions.telnet.TelnetConsole': None,
    'scrapy.extensions.closespider.CloseSpider': 1
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy_selenium.SeleniumMiddleware': 800
# }
#
# SELENIUM_DRIVER_NAME = 'firefox'
# SELENIUM_BROWSER_EXECUTABLE_PATH = which('firefox')
# SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
# SELENIUM_DRIVER_ARGUMENTS=[]


# ITEM_PIPELINES = {
#     'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 500
# }
#
# ELASTICSEARCH_SERVERS = ['localhost']
# ELASTICSEARCH_INDEX = 'scrapy'
# ELASTICSEARCH_INDEX_DATE_FORMAT = '%Y-%m'
# ELASTICSEARCH_TYPE = 'items'
# #ELASTICSEARCH_UNIQ_KEY = 'url'  # Custom unique key
#
# # can also accept a list of fields if need a composite key
# ELASTICSEARCH_UNIQ_KEY = ['nama', 'url']