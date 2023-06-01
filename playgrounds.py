from MongoDbCollectionHandler import MongoDbCollectionHandler

mongodbCollectionHandler = MongoDbCollectionHandler(uri="mongodb+srv://user:netninja@nodetutorial.d7env.mongodb.net/practicingDb?retryWrites=true&w=majority",
                                databaseName="practicingDb", collectionName="dbpracticecollections2", getObjectIds=False)


# print(mongodbCollectionHandler.getAllItems())
# mongodbCollectionHandler.addManyItems([
#     {"title":"lmaoo"},
#     {"title":"ok lol"}
# ])



# print(mongodbCollectionHandler.findOne({"title":"hello world"}))


# mongodbCollectionHandler.replaceAllItems([
#     {"title":"lmaoo"},
#     {"title":"ok lol"}
# ])

print(mongodbCollectionHandler.findOne({"title": "lmaoo"}))