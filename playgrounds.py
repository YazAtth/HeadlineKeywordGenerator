import os
from datetime import datetime

from MongoDbCollectionHandler import MongoDbCollectionHandler

utilityCollection = MongoDbCollectionHandler(uri=os.environ["URI"], databaseName="StateOfNewsApp", collectionName="utils")


rssUrlList = utilityCollection.findOne({"utilType": "rssFeedList"}).get("rssFeedList")

print(rssUrlList)