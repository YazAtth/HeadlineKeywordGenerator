from typing import List

import requests
import xmltodict
import json

class ArticleContainer:
    def __init__(self):
        self.articleList = []
        self.rssUrlList = ["https://www.theguardian.com/international/rss",
                           "http://feeds.bbci.co.uk/news/rss.xml",
                           "http://feeds.bbci.co.uk/news/world/rss.xml",
                           "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"]
        self.idGeneration: int = 0


    def getArticles(self):
        return self.articleList

    def getHeadlines(self) -> List[str]:

        headline_list = []

        for article in self.articleList:
            headline_list.append(article["title"])

        return headline_list



    def _make_api_request(self, url: str):
        res = requests.get(url=url)
        xmlParsed = xmltodict.parse(res.text)

        json_res_as_string = json.dumps(xmlParsed)
        json_res = json.loads(json_res_as_string)

        # print(res.json())

        return json_res

    def getArticlesFromRssFeeds(self) -> None:

        for url in self.rssUrlList:
            json_res = self._make_api_request(url)
            article_list_from_rss_feed = json_res["rss"]["channel"]["item"]

            for article_from_rss_feed in article_list_from_rss_feed:

                article_object = {
                    "article_id": self._generateId(),
                    "title": article_from_rss_feed["title"],
                    "link": article_from_rss_feed["link"],
                    "description": article_from_rss_feed["description"],
                }

                self.articleList.append(article_object)


    def _generateId(self) -> int:
        article_id = self.idGeneration
        self.idGeneration += 1
        return article_id







