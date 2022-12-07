import scrapy


class SpiderSteamItem(scrapy.Item):
    name = scrapy.Field()
    cat = scrapy.Field()
    rating = scrapy.Field()
    release_date = scrapy.Field()
    developer = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    platforms = scrapy.Field()
