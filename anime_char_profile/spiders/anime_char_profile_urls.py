import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json
import os


class AnimeCharProfileUrlsSpider(scrapy.Spider):
    name = "anime_char_profile_urls"
    # allowed_domains = ["imdb.com"]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    data_dir = os.path.join("data")
    base_url = "https://characterprofile.fandom.com"

    
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
        alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        url = (
            AnimeCharProfileUrlsSpider.base_url
            + "/wiki/Category:Anime/Manga_Characters"
        )

        for letter in alphabets:
            next_url = url + "?from=" + str(letter)
            print(next_url)
            yield scrapy.Request(
                url=next_url, headers=self.headers, callback=self.parse
            )

    def parse(self, response):

        # html = ""
        # path = os.path.join(
        #     AnimeCharProfileUrlsSpider.data_dir, "template.html")
        # with open(path, "r", encoding="utf-8") as html_file:
        #     # html_file.write(response.text)
        #     for line in html_file.read():
        #         html += line

        # response = Selector(text=html)

        for character_element in response.css("li.category-page__member"):
            # print(character_element.css("a.category-page__member-link::text").get())
            # print(character_element.css("a.category-page__member-link"))
            # print(character_element.css("a.category-page__member-link::attr('href')").get())
            title = str(
                character_element.css(
                    "a.category-page__member-link::text").get()
            ).strip()
            url = (
                AnimeCharProfileUrlsSpider.base_url
                + str(
                    character_element.css(
                        "a.category-page__member-link::attr('href')"
                    ).get()
                ).strip()
            )
            items = {
                "title": title.encode().decode('unicode_escape'),
                "url": url,
            }
            yield items


    

if __name__ == "__main__":
    # process = AnimeCharProfileUrlsSpider()
    # process.parse("")
    # process.start_requests()

    process = CrawlerProcess()
    process.crawl(AnimeCharProfileUrlsSpider)
    process.start()
