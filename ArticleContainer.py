import os

import regex as re
from typing import List
import requests
import xmltodict
import json

from S3Client import S3Client

s3_client = S3Client()

class ArticleContainer:
    def __init__(self):
        self.savedArticles = {}

        self.rssUrlList = s3_client.read_file_from_s3(bucket_name=os.environ["AWS_S3_BUCKET"], file_name="rss_feeds.txt", is_list=True)
        self.idGeneration: int = 0


    def getArticles(self):
        return self.savedArticles

    def getHeadlines(self) -> List[str]:

        headline_list = []

        for article in self.savedArticles.values():
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

                article_id = self._generateId()
                article_object = {
                    "title": self._remove_html_tags(article_from_rss_feed["title"]),
                    "link": article_from_rss_feed["link"],
                    "description": self._remove_html_tags(str(article_from_rss_feed.get("description", ""))),
                }

                # Guard to prevent duplicate articles
                if article_object["link"] not in obtainedArticleLinks:
                    # self.articleList.append(article_object)
                    self.savedArticles[article_id] = article_object
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





