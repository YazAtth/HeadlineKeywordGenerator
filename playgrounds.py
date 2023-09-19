from S3Client import S3Client
import csv
from io import StringIO


s3_client = S3Client()

input_string = s3_client.read_file_from_s3(bucket_name="sample-cli-test-bucket", file_name="rss_feeds.txt", is_list=True)

print(input_string)



