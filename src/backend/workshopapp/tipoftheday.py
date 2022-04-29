import boto3
import json
from botocore.exceptions import ClientError

class TipOfTheDaySource(object):
    def tips(self):
        return []


class StaticTipOfTheDaySource(TipOfTheDaySource):
    """
        Hardcoded tips
    """

    def tips(self):
        return [
            "Tell them while they're still alive",
            "Be a problem solver, not a problem creator",
            "If you have something nice to say about someone, say it",
            "Focus on the error, not the person",
        ]

class S3TipOfTheDaySource(TipOfTheDaySource):
    """
        Fetch tips from a file in an S3 bucket
    """

    def __init__(self, bucket_name: str, tips_key: str='tips.json', region_name: str='eu-north-1'):
        self.bucket_name = bucket_name
        self.tips_key = tips_key
        self.region_name = region_name
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
        Fetch tips from a DynamoDB table
    """

    def __init__(self, bucket_name: str, table_name: str='tip_of_the_day', region_name: str='eu-north-1'):
        self.bucket_name = bucket_name
        self.table_name = table_name
        self.region_name = region_name
        self.table = boto3.resource('dynamodb').Table(table_name)

    def tips(self):
        try:
            items = self.table.scan()
            return [item['tip']['S'] for item in items]
        except ClientError:
            print(f'Failed when reading dynamodb://{self.table_name}')
            return []
