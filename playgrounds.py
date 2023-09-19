from S3Client import S3Client

s3_client = S3Client()

print(s3_client.read_file_from_s3(bucket_name="sample-cli-test-bucket", file_name="rss_feeds.txt"))


