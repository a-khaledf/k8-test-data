# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MaliciousFileCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    file_urls = scrapy.Field()
    extension = scrapy.Field()
    files = scrapy.Field()
    hash_api_url=scrapy.Field()
