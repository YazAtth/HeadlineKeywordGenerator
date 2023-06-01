import json
from typing import List

import numpy as np

import MatrixGenerator
import NounFrequency
import VisJsParser
from ArticleContainer import ArticleContainer
from MongoDbCollectionHandler import MongoDbCollectionHandler

URI = "mongodb+srv://user:netninja@nodetutorial.d7env.mongodb.net/practicingDb?retryWrites=true&w=majority"

# Grab articles from RSS feeds and place into the database
articleContainer = ArticleContainer()
articleContainer.getArticlesFromRssFeeds()
articleDbCollection = MongoDbCollectionHandler(
    uri=URI,
    databaseName="StateOfNewsApp", collectionName="articles")
articleDbCollection.replaceAllItems(itemList=articleContainer.getArticles())


# Make a graph from the most frequently used keywords from the headlines and put into the database
headlines: List[str] = articleContainer.getHeadlines()
top_nouns: dict[str, int] = NounFrequency.top_nouns(articleContainer.getHeadlines(), 100)

showing_together_matrix: np.array = MatrixGenerator.get_showing_together_matrix(noun_dict=top_nouns,
                                                                                headline_list=headlines)
adjacency_matrix: np.array = MatrixGenerator.get_adjacency_matrix(noun_dict=top_nouns, headline_list=headlines)
nodeEdgeJsonString = VisJsParser.get_visjs_graph_object(noun_dict=top_nouns, adjacency_matrix=adjacency_matrix)

# print(type(json.loads(nodeEdgeJsonString)))

graphDbCollection = MongoDbCollectionHandler(uri=URI, databaseName="StateOfNewsApp", collectionName="graph")
graphDbCollection.replaceAllItems([json.loads(nodeEdgeJsonString)])



# Pair up each node id (representing a keyword from a headline) with the article ids of all of the headlines that it
# has appeared in and save to the database.
nodeList = json.loads(nodeEdgeJsonString)["nodes"]
nodeAndHeadlineForeignKeyPairingList = []

for node in nodeList:

    nodeAndHeadlineForeignKeysObject = {}

    nodeLabel = node["label"].lower()
    nodeAndHeadlineForeignKeysObject["nodeLabel"] = nodeLabel
    nodeAndHeadlineForeignKeysObject["relatedArticleIds"] = []

    for article in articleContainer.getArticles():
        headline = article["title"]
        headline_lowercase = headline.lower()

        if nodeLabel in headline_lowercase.split():
            nodeAndHeadlineForeignKeysObject["relatedArticleIds"].append(article["article_id"])

    nodeAndHeadlineForeignKeyPairingList.append(nodeAndHeadlineForeignKeysObject)

# print(nodeAndHeadlineForeignKeyPairingList)

nodeAndHeadlineJunctionsDbCollection = MongoDbCollectionHandler(uri=URI, databaseName="StateOfNewsApp",
                                                                collectionName="nodeAndHeadlineJunctions")
nodeAndHeadlineJunctionsDbCollection.replaceAllItems(nodeAndHeadlineForeignKeyPairingList)


# print(articleContainer.getArticles())
