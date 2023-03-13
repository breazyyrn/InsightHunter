import scrapy


class FacebookScraperSpider(scrapy.Spider):
    name = "facebook_scraper"
    allowed_domains = ["www.facebook.com"]
    start_urls = ["http://www.facebook.com/"]

    # Custom settings for the spider
    custom_settings = {
        'CONCURRENT_REQUESTS' : 1, # Only one request at a time
        'DOWNLOAD_DELAY' : 5, # Delay between requests
        'ROBOTSTXT_OBEY' : True, # Obey robots.txt tules
        'AUTOTHROTTLE_ENABLED' : True, # Enable autothrottle
        'AUTOTHROTTLE_START_DELAY' : 5, # Initial delay for AutoThrottle
    }

    def __init__(self, user_id=None, *args, **kwargs):
        super(FacebookScraperSpider, self).__init__(*args, **kwargs)
        self.user_id = user_id
        self.start_urls = [f"https://www.facebook.com/{self.user_id}"]

    def parse(self, response):
        # Check if the user profile exists
        if "Page Not Found" in response.xpath('//title/text()').get():
            self.logger.warning(f"User profile {self.user_id} not found.")
            return
        
        # Extract basic profile information
        profile_name = response.xpath('//h1//span/text()').get()
        profile_picture = response.xpath('//img[contains(@class, "profilePic")]/@src').get()
        profile_info = response.xpath('//div[contains(@class, "clearfix")]//div[contains(@class, "_4bl9")]//text()').get()

        # Extract information about friends
        friends_list = []
        friends_url = response.url + "/friends"
        yield scrapy.Request(friends_url, callback=self.parse_friends)

        # Extract information about pages interacted with
        pages_list = []
        pages_url = response.url + "/pages"
        yield scrapy.Request(pages_url, callback=self.parse_pages)

        # Yielf a dictionary containing the extracted information
        yield {
            'profile_name': profile_name,
            'profile_picture': profile_picture,
            'profile_info': profile_info,
            'friends_list': friends_list,
            'pages_list': pages_list
        }

    def parse_friends(self, response):
            # Extract the list of friends
        
    def parse_pages(self, response):
            # Extract the list of pages interacted with
        
    def parse_colby(self, response):
            # Parse the Colby Website and extract information

    def parse_linkedin(self, response):
            # Parse the LinkedIn Website and extract information
    

        pass
