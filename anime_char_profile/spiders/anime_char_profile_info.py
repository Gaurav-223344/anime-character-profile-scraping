import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json
import os

class AnimeCharProfileInfoSpider(scrapy.Spider):
    name = "anime_char_profile_info"
    allowed_domains = ["characterprofile.fandom.com"]
    
    data_dir = os.path.join("data")
    
    custom_settings = {
        'FEEDS': {
            os.path.join(data_dir, 'anime_char_profile_urls.json'): {
                'format': 'json',
                'encoding': 'utf8',
                'overwrite': True,
            },
        },
        "LOG_FILE": "logs/anime_char_profile_urls.log",
    }

    
    def start_requests(self):
        
        with open(os.path.join(AnimeCharProfileInfoSpider.data_dir, "anime_char_profile_urls.json"), 'r', encoding="utf-8") as json_file:
            json_data = json.load(json_file)

        for anime_char_dict in json_data:
            title = anime_char_dict.get("title")
            if("Category:" in title ): continue
            url = anime_char_dict.get("url")
            # urlsss.append(url)
            break
        print(url)
        # print(len(urlss))

    def parse(self, response):
        pass


if __name__ == "__main__":
    process = AnimeCharProfileInfoSpider()
    # process.parse("")
    process.start_requests()

    # process = CrawlerProcess()
    # process.crawl(AnimeCharProfileInfoSpider)
    # process.start()