import boto3 as boto3


class S3Client:

    def __init__(self):
        self.s3_client = boto3.client('s3')

    # 'sample-cli-test-bucket'
    def read_file_from_s3(self, bucket_name, file_name):
        obj = self.s3_client.get_object(Bucket=bucket_name, Key=file_name)
        data = obj['Body'].read()
        return str(data).split('\'')[1].replace("\\n", "\n")

    def write_to_s3_file(self, data_string, bucket_name, key_name):
        self.s3_client.put_object(
            Body=data_string,
            Bucket=bucket_name,
            Key=key_name
        )
