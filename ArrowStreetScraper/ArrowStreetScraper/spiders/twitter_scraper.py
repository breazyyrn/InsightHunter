import scrapy


class TwitterScraperSpider(scrapy.Spider):
    name = "twitter_scraper"
    allowed_domains = ["www.twitter.com"]
    start_urls = ["http://www.twitter.com/"]

    def parse(self, response):
        pass
