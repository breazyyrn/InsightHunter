import scrapy


class ColbyScraperSpider(scrapy.Spider):
    name = "colby_scraper"
    allowed_domains = ["www.colby.edu"]
    start_urls = ["http://www.colby.edu/"]

    def parse(self, response):
        # Extract the title of the page
        title = response.xpath('//title/text()').get()

        # Extract the text from the page
        text = response.xpath('//body//text()').getall()
        text = ''.join(text).strip()

        # Extract the links on the page
        links = response.xpath('//a/@href').getall()

        # Yield a dictionary containing the extracted information
        yield {
            'title': title,
            'text': text,
            'links': links
        }
        pass
