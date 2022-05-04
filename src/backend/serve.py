from os import environ

from workshopapp.server import SocketServerTipOfTheDayServer
from workshopapp.tipoftheday import StaticTipOfTheDaySource

def get_tip_source():
    s3_bucket = environ.get('S3_BUCKET', None)
    aws_region = environ.get('AWS_DEFAULT_REGION', 'eu-north-1')

    if s3_bucket:
        from workshopapp.tipoftheday.aws import S3TipOfTheDaySource
        return S3TipOfTheDaySource(bucket_name=s3_bucket, region_name=aws_region)

    dynamodb_table = environ.get('DYNAMODB_TABLE', None)
    if dynamodb_table:
        from workshopapp.tipoftheday.aws import DynamoDBTipOfTheDaySource
        return DynamoDBTipOfTheDaySource(table_name=dynamodb_table, region_name=aws_region)

    return StaticTipOfTheDaySource()

if __name__ == '__main__':
    tip_source = get_tip_source()
    print(f'Using tip source: {type(tip_source).__name__}')

    host = SocketServerTipOfTheDayServer(tip_source=tip_source)

    host.serve()