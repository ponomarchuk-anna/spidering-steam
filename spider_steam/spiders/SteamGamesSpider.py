import scrapy
from spider_steam.items import SpiderSteamItem


class SteamgamesspiderSpider(scrapy.Spider):
    name = 'SteamGamesSpider'
    allowed_domains = [
        'steam.com',
        'steampowered.com',
        ]
    start_urls = [
        'https://store.steampowered.com/search/?tags=492&ndl=1&page=1',
        'https://store.steampowered.com/search/?tags=19&ndl=1&page=1',
        'https://store.steampowered.com/search/?tags=3871&ndl=1&page=1',
        'https://store.steampowered.com/search/?tags=492&ndl=1&page=2',
        'https://store.steampowered.com/search/?tags=19&ndl=1&page=2',
        'https://store.steampowered.com/search/?tags=3871&ndl=1&page=2',
    ]

    def parse_game(self, response):
        items = SpiderSteamItem()
        name = response.xpath('//div[@id="appHubAppName"]/text()').extract()
        if name:
            date = response.xpath('//div[@class="date"]/text()').extract()[0]
            if int(date.split(' ')[-1]) > 2000:
                items['name'] = name[0]

                price = response.xpath('//div[@class="game_purchase_action"]//div[contains(@class, "game_purchase_price")]/text()').extract()
                if price:
                    items['price'] = price[0].strip()
                else:
                    try:
                        items['price'] = response.xpath('//div[@class="game_purchase_action"]//div[contains(@class, "discount_final_price")]/text()').extract()[0].strip()
                    except IndexError:
                        items['price'] = 'Free to Play'

                items['cat'] = ' > '.join(response.xpath('//div[@class="blockbg"]//a/text()').extract()[1:])

                counter = response.xpath('//span[@class="responsive_hidden"]/text()').extract()[-2].strip()[1:-1].replace(',', '')
                rating = response.xpath('//span[contains(@class, "game_review_summary")]/text()').extract()[-2]
                items['rating'] = (rating, counter)

                items['release_date'] = date
                items['developer'] = response.xpath('//div[@id="developers_list"]/a/text()').extract()
                items['tags'] = response.xpath('//div[@class="game_area_features_list_ctn"]//div[@class="label"]/text()').extract()
                platforms = set(response.xpath('//div[@class="game_area_purchase_platform"]//span/@class').extract())
                items['platforms'] = [p.split()[1] for p in platforms if 'music' not in p and ' ' in p]
                yield items

    def parse(self, response):
        urls = response.xpath('//div[@id="search_resultsRows"]/a/@href').extract()
        for url in urls:
            yield response.follow(url=url, callback=self.parse_game)
