import requests
import xmltodict
import json

class HeadlineRetriever:
    def __init__(self):
        self.headlineList = []
        self.rssUrlList = ["https://www.theguardian.com/international/rss",
                           "http://feeds.bbci.co.uk/news/rss.xml",
                           "http://feeds.bbci.co.uk/news/world/rss.xml",
                           "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"]

    def make_api_request(self, url: str):
        res = requests.get(url=url)
        xmlParsed = xmltodict.parse(res.text)

        json_res_as_string = json.dumps(xmlParsed)
        json_res = json.loads(json_res_as_string)

        # print(res.json())

        return json_res

    def setHeadlineList(self) -> None:

        for url in self.rssUrlList:
            json_res = self.make_api_request(url)
            article_list = json_res["rss"]["channel"]["item"]

            for article in article_list:
                self.headlineList.append(article["title"])









