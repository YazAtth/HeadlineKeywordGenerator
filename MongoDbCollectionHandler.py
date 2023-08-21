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
    def __init__(self, uri, databaseName, collectionName, getObjectIds=True):
        self.client = MongoClient(uri)
        self.db = self.client[databaseName]
        self.collection = self.db[collectionName]
        self.getObjectIds = getObjectIds


    def getAllItems(self):
        json_objects = []

        if self.getObjectIds:
            for item in self.collection.find({}):
                json_objects.append(item)
        else:
            for item in self.collection.find({}, {"_id": 0}):
                json_objects.append(item)

        return json_objects

    def findOne(self, query):
        if self.getObjectIds:
            return self.collection.find_one(query)
        else:
            print("ran")
            return self.collection.find_one(query, {"_id": 0})


    def findMany(self, query):
        json_objects = []

        if self.getObjectIds:
            for item in self.collection.find(query):
                json_objects.append(item)
        else:
            for item in self.collection.find(query, {"_id": 0}):
                json_objects.append(item)


        return json_objects


    def addOneItem(self, item):
        self.collection.insert_one(item)

    def addManyItems(self, itemList):
        self.collection.insert_many(itemList)


    def replaceAllItems(self, itemList):
        self.collection.delete_many({})
        self.addManyItems(itemList)

    def replaceItemBy(self, item, delete_filter):
        self.collection.delete_one(delete_filter)
        self.addOneItem(item)