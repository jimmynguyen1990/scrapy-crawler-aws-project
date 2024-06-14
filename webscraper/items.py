# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class WebscraperItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class WebItem(scrapy.Item):
    title = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    serial = scrapy.Field()
    link = scrapy.Field()
    proposal_deadline = scrapy.Field()
    organizer = scrapy.Field()
    city = scrapy.Field()
    nation = scrapy.Field()
