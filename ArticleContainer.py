import regex as re
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
                           "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
                           "http://rss.cnn.com/rss/cnn_topstories.rss",
                           "https://www.huffpost.com/section/front-page/feed?x=1",
                           "https://cdn.feedcontrol.net/8/1114-wioSIX3uu8MEj.xml",
                           "https://www.rte.ie/feeds/rss/?index=/news/&limit=100",
                           "https://www.irishtimes.com/arc/outboundfeeds/feed-irish-news/?from=0&size=100"]
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
        obtainedArticleLinks = []  # Keep track of added articles prevent the same article from being added twice

        for url in self.rssUrlList:
            json_res = self._make_api_request(url)
            article_list_from_rss_feed = json_res["rss"]["channel"]["item"]

            for article_from_rss_feed in article_list_from_rss_feed:

                # If headline is empty
                if not article_from_rss_feed["title"]:
                    continue


                article_object = {
                    "article_id": self._generateId(),
                    "title": self._remove_html_tags(article_from_rss_feed["title"]),
                    "link": article_from_rss_feed["link"],
                    "description": self._remove_html_tags(str(article_from_rss_feed.get("description", ""))),
                }

                # Guard to prevent duplicate articles
                if article_object["link"] not in obtainedArticleLinks:
                    self.articleList.append(article_object)
                    obtainedArticleLinks.append(article_object["link"])


    def _generateId(self) -> int:
        article_id = self.idGeneration
        self.idGeneration += 1
        return article_id

    def _remove_html_tags(self, string):

        # If string is empty
        if not string:
            return string


        # Define the regular expression pattern to match HTML tags
        pattern = re.compile(r'<.*?>')

        # Remove HTML tags from the string using the pattern
        result = re.sub(pattern, '', str(string))

        return result





