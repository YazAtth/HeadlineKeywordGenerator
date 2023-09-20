import os

from S3Client import S3Client
import csv
from io import StringIO

def awsFunc():
    s3_client = S3Client()
    input_string = s3_client.read_file_from_s3(bucket_name="sample-cli-test-bucket", file_name="graph_data.json")
    print(input_string)

# def mongoFunc():
#     utilityCollection = MongoDbCollectionHandler(uri=os.environ["URI"], databaseName="StateOfNewsApp", collectionName="graph")
#     custom_stop_word_list = utilityCollection.getAllItems()
#     print(custom_stop_word_list)


awsFunc()
# mongoFunc()