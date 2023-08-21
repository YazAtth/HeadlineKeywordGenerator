from datetime import datetime

from MongoDbCollectionHandler import MongoDbCollectionHandler

URI = "mongodb+srv://user:netninja@nodetutorial.d7env.mongodb.net/practicingDb?retryWrites=true&w=majority"
utilityCollection = MongoDbCollectionHandler(uri=URI, databaseName="StateOfNewsApp", collectionName="utils")

utilItem = {
    "utilType": "lastUpdated",
    "lastUpdated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
# utilityCollection.replaceAllItems([utilItem])
utilityCollection.replaceItemBy(utilItem, {"utilType": "lastUpdated"})