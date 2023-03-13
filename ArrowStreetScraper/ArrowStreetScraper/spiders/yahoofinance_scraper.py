import scrapy


class YahoofinanceScraperSpider(scrapy.Spider):
    name = "yahoofinance_scraper"
    allowed_domains = ["www.finance.yahoo.com"]
    start_urls = ["http://www.finance.yahoo.com/"]

    def parse(self, response):
        pass
