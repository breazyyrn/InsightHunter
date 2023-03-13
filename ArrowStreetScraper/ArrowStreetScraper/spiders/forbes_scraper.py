import scrapy


class ForbesScraperSpider(scrapy.Spider):
    name = "forbes_scraper"
    allowed_domains = ["www.forbes.com"]
    start_urls = ["http://www.forbes.com/"]

    def parse(self, response):
        # Extract the list of articles
        articles = response.xpath('//div[contains(@class, "search-result-card")]')

        # Extract infromaton from each article
        for article in articles:
            title = article.xpath('.//h2/a/text()').get()
            author = article.xpath('.//span[contains(@class, "fs-name")]/text()').get()
            date = article.xpath('.//time[contains(@class, "date")]/@datetime').get()
            url = article.xpath('.//h2/a/@href').get()

        # Yielf a dictionary containing the extracted information
        yield {
            'title': title,
            'author': author,
            'date': date,
            'url': url  
        }
        pass
