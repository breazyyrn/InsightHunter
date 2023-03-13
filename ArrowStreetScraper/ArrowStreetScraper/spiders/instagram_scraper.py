import scrapy
import difflib
import nltk
import spacy
from datetime import datetime, timedelta
import json

# Define the list of other spiders' scoped data to be used in the profile verifier engine
linkedin_data = []
twitter_data = []
facebook_data = []

# Define the similarity threshold for the profile verifier
SIMILARITY_THRESHOLD = 0.8

# Define the cache expiration time in minutes
CACHE_EXPIRATION_TIME = 60

# Define the cache for the profile verifier
profile_cache = {}

# Initialize the spacy NER model
nlp = spacy.load("en_core_web_sm")

# Define the function to verify the scraped user's profile
def verify_profile(user_data):
    # Check if the user's profile data is already cached
    if user_data['username'] in profile_cache:
        cached_data, cached_timestamp = profile_cache[user_data['username']]
        # Check if the cached data is still valid
        if datetime.now() - cached_timestamp <= timedelta(minutes=CACHE_EXPIRATION_TIME):
            if cached_data == user_data:
                return True
            else:
                # Calculate the similarity score between the cached data and the new data
                similarity_score = 0
                for key in user_data.keys():
                    if key != 'profile_picture':
                        if key in cached_data:
                            # Tokenize the text fields and compare using the difflib library
                            if isinstance(user_data[key], str) and isinstance(cached_data[key], str):
                                user_tokens = set(nltk.word_tokenize(user_data[key].lower()))
                                cached_tokens = set(nltk.word_tokenize(cached_data[key].lower()))
                                similarity_score += difflib.SequenceMatcher(None, user_tokens, cached_tokens).ratio()
                            # Extract and compare named entities using spacy
                            else:
                                user_entities = set([ent.text for ent in nlp(user_data[key]) if ent.label_ in ['PERSON', 'ORG', 'LOC']])
                                cached_entities = set([ent.text for ent in nlp(cached_data[key]) if ent.label_ in ['PERSON', 'ORG', 'LOC']])
                                similarity_score += len(user_entities & cached_entities) / len(user_entities | cached_entities)
                similarity_score /= len(user_data.keys())
                # Check if the similarity score is above the threshold
                if similarity_score >= SIMILARITY_THRESHOLD:
                    # Update the cache with the new data
                    profile_cache[user_data['username']] = (user_data, datetime.now())
                    return True
                else:
                    return False
        else:
            # Discard the cached data if it's too old
            del profile_cache[user_data['username']]

class InstagramScraperSpider(scrapy.Spider):
    name = "instagram_scraper"
    start_urls = ["https://www.instagram.com/"]

    def parse(self, response):
        # Extract the list of users
        users = response.xpath('//ul[contains(@class, "jSC57")]//a')

        # Extract information from each user's profile
        for user in users:
            username = user.xpath('./@href').get()[1:]
            full_name = user.xpath('./div/div/div/div/div/text()').get()
            biography = user.xpath('./div/div/div/div/span/text()').get()
            follower_count = user.xpath('./div/div/div/div/span[contains(@class, "-by3EC")]/@title').get()
            following_count = user.xpath('./div/div/div/div/span/a[contains(@href, "following")]/span/text()').get()
            post_count = user.xpath('./div/div/div/div/span/a[contains(@href, "posts")]/span/text()').get()

            # Construct the user's profile data dictionary
            user_data = {
                "username": username,
                "full_name": full_name,
                "profile_picture": "",
                "bio": biography,
                "website": "",
                "is_private": False,
                "is_verified": False,
                "followed_by": follower_count,
                "follows": following_count,
                "media_count": post_count,
                "media": []
            }

            # Verify if the user's profile data is already scraped
            if verify_profile(user_data):
                continue

            # Scrape the user's profile data
            user_profile_url = f"https://www.instagram.com/{username}/?__a=1"
            yield scrapy.Request(user_profile_url, callback=self.parse_user_profile, meta={"user_data": user_data})
    def parse_user_profile(self, response):
        user_data = response.meta["user_data"]
        data = json.loads(response.text)["graphql"]["user"]

        # Extract the user's profile data
        user_data["profile_picture"] = data["profile_pic_url_hd"]
        user_data["bio"] = data["biography"]
        user_data["website"] = data["external_url"]
        user_data["is_private"] = data["is_private"]
        user_data["is_verified"] = data["is_verified"]
        user_data["followed_by"] = data["edge_followed_by"]["count"]
        user_data["follows"] = data["edge_follow"]["count"]
        user_data["media_count"] = data["edge_owner_to_timeline_media"]["count"]

        # Extract the user's media
        media = data["edge_owner_to_timeline_media"]["edges"]
        for node in media:
            if node["node"]["is_video"]:
                media_type = "video"
                media_url = node["node"]["video_url"]
            else:
                media_type = "photo"
                media_url = node["node"]["display_url"]
            # Add the medi a data to the user_data dictionary
            user_data["media"].append({"type": media_type, "url": media_url})

