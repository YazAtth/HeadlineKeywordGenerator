import os
from datetime import datetime

from MongoDbCollectionHandler import MongoDbCollectionHandler

utilityCollection = MongoDbCollectionHandler(uri=os.environ["URI"], databaseName="StateOfNewsApp", collectionName="utils")

utilItem = {
    "utilType": "lastUpdated",
    "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
# utilityCollection.replaceAllItems([utilItem])
utilityCollection.replaceItemBy(utilItem, {"utilType": "lastUpdated"})