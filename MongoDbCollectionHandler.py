from pymongo import MongoClient
# from mongoengine import Document, ListField, StringField, URLField



#
# allCollectionItems = collection.find({})
# collection.insert_one({
#     "sourceTitle":"The news",
#     "title":"hello world",
#     "lol":"ok"
#
# })


# for item in allCollectionItems:
#     print(item["title"])


class MongoDbCollectionHandler:
    def __init__(self, uri, databaseName, collectionName):
        self.client = MongoClient(uri)
        self.db = self.client[databaseName]
        self.collection = self.db[collectionName]


    def getAllItems(self):
        json_objects = []

        for item in self.collection.find({}):
            json_objects.append(item)

        return json_objects


    def addOneItem(self, item):
        self.collection.insert_one(item)

    def addManyItems(self, itemList):
        self.collection.insert_many(itemList)