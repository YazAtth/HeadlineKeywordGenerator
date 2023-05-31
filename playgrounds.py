from MongoDbCollectionHandler import MongoDbCollectionHandler

mongodbCollectionHandler = MongoDbCollectionHandler("mongodb+srv://user:netninja@nodetutorial.d7env.mongodb.net/practicingDb?retryWrites=true&w=majority",
                                "practicingDb", "dbpracticecollections2")


print(mongodbCollectionHandler.getAllItems())
mongodbCollectionHandler.addManyItems([
    {"title":"lmaoo"},
    {"title":"ok lol"}
])
