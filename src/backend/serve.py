from os import environ

from workshopapp.server import SocketServerTipOfTheDayServer
from workshopapp.tipoftheday import StaticTipOfTheDaySource

def create_s3_tip_source(bucket):
    from workshopapp.tipoftheday.aws import S3TipOfTheDaySource
    return S3TipOfTheDaySource(bucket_name=bucket)

def create_dynamodb_tip_source(table):
    aws_region = environ.get('AWS_DEFAULT_REGION', 'eu-north-1')

    from workshopapp.tipoftheday.aws import DynamoDBTipOfTheDaySource
    return DynamoDBTipOfTheDaySource(table_name=table, region_name=aws_region)

def get_tip_source():
    """
        pick and configue tip source to use.

        If the environment variable 'S3_BUCKET' is set, an S3TipOfTheDaySource
        will be created with the bucket_name set to the value of 'S3_BUCKET'

        If the environment variable 'DYNAMODB_TABLE' is set, a DynamoDBTipOfTheDaySource
        will be created with the table_name set to the value of 'DYNAMODB_TABLE'
    """
    s3_bucket = environ.get('S3_BUCKET', None)
    dynamodb_table = environ.get('DYNAMODB_TABLE', None)

    if s3_bucket:
        return create_s3_tip_source(s3_bucket)
    
    if dynamodb_table:
        return create_dynamodb_tip_source(dynamodb_table)

    return StaticTipOfTheDaySource()

if __name__ == '__main__':
    tip_source = get_tip_source()
    print(f'Using tip source: {type(tip_source).__name__}')

    host = SocketServerTipOfTheDayServer(tip_source=tip_source)

    host.serve()