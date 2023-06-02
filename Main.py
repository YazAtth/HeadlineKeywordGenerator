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
top_nouns_and_plural_hash = NounFrequency.get_top_nouns_and_plural_hash(articleContainer.getHeadlines(), 100)
top_nouns: dict[str, int] = top_nouns_and_plural_hash[0]

# We get the plural to non_plural map by reversing the existing map
non_plural_to_original_map: dict[str, str] = top_nouns_and_plural_hash[1]
original_to_non_plural_map: dict[str, str] = {value: key for key, value in non_plural_to_original_map.items()}

showing_together_matrix: np.array = MatrixGenerator.get_showing_together_matrix(noun_dict=top_nouns,
                                                                                headline_list=headlines)
adjacency_matrix: np.array = MatrixGenerator.get_adjacency_matrix(noun_dict=top_nouns, headline_list=headlines)
nodeEdgeJsonString = VisJsParser.get_visjs_graph_object(noun_dict=top_nouns, adjacency_matrix=adjacency_matrix)


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
        headline = article["title"].lower()
        headline_lowercase = headline.lower()
        headline_lowercase = headline_lowercase.replace("’", " ")  # Replaces all apostrophes with a space
        headline_lowercase = headline_lowercase.replace(":", " ")  # Replaces all colons with a space


        # Remove punctuation in the headline
        headline_word_list = [headline_word for headline_word in headline_lowercase.split() if headline_word.isalnum()]


        if nodeLabel in headline_word_list:
            nodeAndHeadlineForeignKeysObject["relatedArticleIds"].append(article["article_id"])
        elif nodeLabel in original_to_non_plural_map:  # Checks the non-plural version of the word to see if it exists there
            if original_to_non_plural_map.get(nodeLabel) in headline_word_list:
                nodeAndHeadlineForeignKeysObject["relatedArticleIds"].append(article["article_id"])




    # Ensure no nodes with an empty relatedArticleId is added.
    if len(nodeAndHeadlineForeignKeysObject["relatedArticleIds"]) > 0:
        nodeAndHeadlineForeignKeyPairingList.append(nodeAndHeadlineForeignKeysObject)
    else:
        print(f"The node: {nodeLabel} has an empty relatedArticleId list")

nodeAndHeadlineJunctionsDbCollection = MongoDbCollectionHandler(uri=URI, databaseName="StateOfNewsApp",
                                                                collectionName="nodeAndHeadlineJunctions")
nodeAndHeadlineJunctionsDbCollection.replaceAllItems(nodeAndHeadlineForeignKeyPairingList)

