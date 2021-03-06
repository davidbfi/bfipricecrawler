#
#
# from bfipricecrawler.items import MyItem
#
#
# class ReviewspiderSpider(scrapy.Spider):
#     name = 'reviewspider'
#     allowed_domains = ["amazon.in"]
#     start_urls = ["https://www.amazon.in/Fossil-Touchscreen-Smartwatch-Smartphone-Notifications/dp/B07SRVV8V4/"]
#
#     def parse(self, response):
#         # This will get the link for the all reviews tag on amazon page.
#         all_reviews = response.xpath(
#             '//div[@data-hook="reviews-medley-footer"]//a[@data-hook="see-all-reviews-link-foot"]/@href').extract_first()
#         # This will tell scrapy to move to all reviews page for further scraping.
#         yield response.follow("https://www.amazon.in" + all_reviews, callback=self.parse_page)
#
#     def parse_page(self, response):
#         # Scraping all the items for all the reviewers mentioned on that Page
#
#         names = response.xpath('//div[@data-hook="review"]//span[@class="a-profile-name"]/text()').extract()
#         reviewerLink = response.xpath('//div[@data-hook="review"]//a[@class="a-profile"]/@href').extract()
#         reviewTitles = response.xpath('//a[@data-hook="review-title"]/span/text()').extract()
#         reviewBody = response.xpath('//span[@data-hook="review-body"]/span').xpath('normalize-space()').getall()
#         verifiedPurchase = response.xpath('//span[@data-hook="avp-badge"]/text()').extract()
#         postDate = response.xpath('//span[@data-hook="review-date"]/text()').extract()
#         starRating = response.xpath('//i[@data-hook="review-star-rating"]/span[@class="a-icon-alt"]/text()').extract()
#         helpful = response.xpath('//span[@class="cr-vote"]//span[@data-hook="helpful-vote-statement"]/text()').extract()
#
#
#         for (name, reviewLink, title, Review, Verified, date, rating, helpful_count) in zip(names, reviewerLink,
#                                                                                             reviewTitles, reviewBody,
#                                                                                             verifiedPurchase, postDate,
#                                                                                             starRating, helpful):
#             # Getting the Next Page URL for futher scraping.
#             next_urls = response.css('.a-last > a::attr(href)').extract_first()
#
#             yield MyItem(names=name, reviewerLink=reviewLink, reviewTitles=title, reviewBody=Review,
#                          verifiedPurchase=Verified, postDate=date, starRating=rating, helpful=helpful_count,
#                          nextPage=next_urls)
#
