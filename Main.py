import json
from typing import List

import numpy as np

import MatrixGenerator
import NounFrequency
import VisJsParser
from ArticleContainer import ArticleContainer


articleContainer = ArticleContainer()
articleContainer._getArticlesFromRssFeeds()

headlines: List[str] = articleContainer.getHeadlines()
top_nouns: dict[str, int] = NounFrequency.top_nouns(articleContainer.getHeadlines(), 100)


showing_together_matrix: np.array = MatrixGenerator.get_showing_together_matrix(noun_dict=top_nouns, headline_list=headlines)
adjacency_matrix: np.array = MatrixGenerator.get_adjacency_matrix(noun_dict=top_nouns, headline_list=headlines)




# print(VisJsParser.noun_dict_to_visjs_nodes(noun_dict=top_nouns))
# print(MatrixGenerator.get_adjacency_matrix(noun_dict=top_nouns, headline_list=headlines))
# print(VisJsParser.adjacency_matrix_to_visjs_edges(adjacency_matrix=adjacency_matrix))

nodeEdgeJsonString = VisJsParser.get_visjs_graph_object(noun_dict=top_nouns, adjacency_matrix=adjacency_matrix)



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

        if nodeLabel in headline_lowercase:
            nodeAndHeadlineForeignKeysObject["relatedArticleIds"].append(article["article_id"])

    nodeAndHeadlineForeignKeyPairingList.append(nodeAndHeadlineForeignKeysObject)

print(nodeAndHeadlineForeignKeyPairingList)




# print(articleContainer.getArticles())




