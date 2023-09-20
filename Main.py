import os
from datetime import datetime
import json
from typing import List
import numpy as np

import MatrixGenerator
import NounFrequency
import VisJsParser
from ArticleContainer import ArticleContainer
from S3Client import S3Client

s3_client = S3Client()

def run():


    # Grab articles from RSS feeds
    articleContainer = ArticleContainer()
    articleContainer.getArticlesFromRssFeeds()


    # articleDbCollection = MongoDbCollectionHandler(
    #     uri=os.environ["URI"],
    #     databaseName="StateOfNewsApp", collectionName="articles")


    # Make a graph from the most frequently used keywords from the headlines
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


    # graphDbCollection = MongoDbCollectionHandler(uri=os.environ["URI"], databaseName="StateOfNewsApp", collectionName="graph")



    # Pair up each node id (representing a keyword from a headline) with the article ids of all of the headlines that it
    # has appeared in and save to the database.
    nodeList = nodeEdgeJsonString["nodes"]
    # nodeAndHeadlineForeignKeyPairingList = []
    nodeAndHeadlineForeignKeyPairingDict = {}

    # TODO: Logic to detect if a key is an empty list and delete the key
    for node in nodeList:

        # nodeAndHeadlineForeignKeysObject = {}

        nodeLabel = node["label"].lower()
        # nodeAndHeadlineForeignKeyPairingDict["nodeLabel"] = nodeLabel
        # nodeAndHeadlineForeignKeyPairingDict["relatedArticleIds"] = []


        for article in articleContainer.getArticles():
            headline = article["title"].lower()
            headline_lowercase = headline.lower()
            headline_lowercase = headline_lowercase.replace("’", " ")  # Replaces all apostrophes with a space
            headline_lowercase = headline_lowercase.replace(":", " ")  # Replaces all colons with a space


            # Remove punctuation in the headline
            headline_word_list = [headline_word for headline_word in headline_lowercase.split() if headline_word.isalnum()]


            if nodeLabel in headline_word_list:
                nodeAndHeadlineForeignKeyPairingDict.setdefault(nodeLabel, []).append(article["article_id"])
            elif nodeLabel in original_to_non_plural_map:  # Checks the non-plural version of the word to see if it exists there
                if original_to_non_plural_map.get(nodeLabel) in headline_word_list:
                    nodeAndHeadlineForeignKeyPairingDict.setdefault(nodeLabel, []).append(article["article_id"])




        # # Ensure no nodes with an empty relatedArticleId is added.
        # if len(nodeAndHeadlineForeignKeysObject["relatedArticleIds"]) > 0:
        #     nodeAndHeadlineForeignKeyPairingList.append(nodeAndHeadlineForeignKeysObject)
        # else:
        #     print(f"The node: {nodeLabel} has an empty relatedArticleId list")

    # nodeAndHeadlineJunctionsDbCollection = MongoDbCollectionHandler(uri=os.environ["URI"], databaseName="StateOfNewsApp",
    #                                                                 collectionName="nodeAndHeadlineJunctions")

    # with open("keyword_to_article_id_hash.json", "w") as f:
    #     json.dump(nodeAndHeadlineForeignKeyPairingDict, f)



    # Pushing to database must happen at the end to preserve atomicity
    # articleDbCollection.replaceAllItems(itemList=articleContainer.getArticles())



    # graphDbCollection.replaceAllItems([json.loads(nodeEdgeJsonString)])

    articles = articleContainer.getArticles()
    # temporarily until we remove the mongoose system that implements the _id field
    # for article in articles:
    #     print(article)
    #     del article["_id"]

    s3_client.write_to_s3_file(
        data_string=json.dumps(articles),
        bucket_name=os.environ["AWS_S3_BUCKET"],
        key_name="articles.txt"
    )
    #
    # with open("articles.txt", "w") as f:
    #     articles = articleContainer.getArticles()
    #
    #     # temporarily until we remove the mongoose system that implements the _id field
    #     for article in articles:
    #         del article["_id"]
    #
    #     json.dump(articles, f)




    s3_client.write_to_s3_file(
        data_string=json.dumps(nodeEdgeJsonString),
        bucket_name=os.environ["AWS_S3_BUCKET"],
        key_name="graph-data.json"
    )

    # nodeAndHeadlineJunctionsDbCollection.replaceAllItems(nodeAndHeadlineForeignKeyPairingList)
    s3_client.write_to_s3_file(
        data_string=json.dumps(nodeAndHeadlineForeignKeyPairingDict),
        bucket_name=os.environ["AWS_S3_BUCKET"],
        key_name="keyword_to_article_id_hash.json"
    )

    # Util collection for debugging
    # utilityCollection = MongoDbCollectionHandler(uri=os.environ["URI"], databaseName="StateOfNewsApp", collectionName="utils")
    # lastUpdatedUtil = {
    #     "utilType": "lastUpdated",
    #     "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # }
    # utilityCollection.replaceItemBy(lastUpdatedUtil, {"utilType": "lastUpdated"})

run()


