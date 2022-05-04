import boto3
import json
from botocore.exceptions import ClientError
from workshopapp.tipoftheday import TipOfTheDaySource

class S3TipOfTheDaySource(TipOfTheDaySource):
    """
        Fetch tips from a file in an S3 bucket
    """

    def __init__(self, bucket_name: str, tips_key: str='tips.json'):
        self.bucket_name = bucket_name
        self.tips_key = tips_key
        self.bucket = boto3.resource('s3').Bucket(bucket_name)

    def tips(self):
        try:
            body = self.bucket.Object(self.tips_key).get()['Body'].read()

            return json.loads(body)
        except ClientError as e:
            error = e.response.get('Error', None)
            code = error.get('Code', None) if error else None

            if code == 'NoSuchKey':
                print(f'No such file s3://{self.bucket_name}/{self.tips_key}')
                return []

            print(f'Failed when reading s3://{self.bucket_name}/{self.tips_key}')
            return []

class DynamoDBTipOfTheDaySource(TipOfTheDaySource):
    """
        Fetch tips from a DynamoDB table.
        The table is scanned for all tips and expects a string attribute with the name 'tip' for each item
    """

    def __init__(self, table_name: str='tip_of_the_day', region_name: str='eu-north-1'):
        self.table_name = table_name
        self.region_name = region_name
        self.session = boto3.Session(region_name=self.region_name)
        self.table = self.session.resource('dynamodb').Table(table_name)

    def tips(self):
        try:
            items = self.table.scan()
            return [item['tip'] for item in items['Items']]
        except ClientError:
            print(f'Failed when reading dynamodb://{self.table_name}')
            return []
