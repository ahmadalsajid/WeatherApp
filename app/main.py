import os
import aiohttp
import boto3
import json
from typing import Union
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dateutil.tz import tzlocal
from fastapi_utilities import repeat_every

load_dotenv()

WEATHER_KEY = os.getenv('OPEN_WEATHER_API_KEY')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'test')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'test')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'weather')
DYNAMODB_TABLE_NAME = os.getenv('DYNAMODB_TABLE_NAME', 'Logs')

s3 = boto3.client(
    service_name='s3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url='http://localstack:4566',
)

dynamodb = boto3.client(
    service_name='dynamodb',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url='http://localstack:4566',
    region_name='us-east-1'
)
app = FastAPI()


# create an S3 bucket and DynamoDB table on startup to
@app.on_event('startup')
async def create_aws_resources():
    s3.create_bucket(Bucket=S3_BUCKET_NAME)
    try:
        response = dynamodb.create_table(
            TableName='logs',
            KeySchema=[
                {
                    'AttributeName': 'log_id',
                    'KeyType': 'HASH'  # Partition_key
                },
                {
                    'AttributeName': 'timestamp',
                    'KeyType': 'RANGE'  # Sort_key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'log_id',
                    'AttributeType': 'N'  # Partition_key
                },
                {
                    'AttributeName': 'timestamp',
                    'AttributeType': 'S'  # Sort_key
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        print(response)
    except Exception as e:
        print(e)


# set a cron job to clean up the S3 bucket from files created more than 5 minutes ago.
@app.on_event('startup')
@repeat_every(seconds=10)
async def clean_s3_files():
    r = s3.list_objects(Bucket=S3_BUCKET_NAME)
    _data = r.get('Contents')
    if _data:
        condition_timestamp = datetime.now(tz=tzlocal()) - timedelta(minutes=5)
        paginator = s3.get_paginator('list_objects_v2')

        s3_filtered_list = [obj for page in paginator.paginate(Bucket=S3_BUCKET_NAME) for obj in page["Contents"] if
                            obj['LastModified'] < condition_timestamp]

        if s3_filtered_list:
            for elem in s3_filtered_list:
                response = s3.delete_object(
                    Bucket=S3_BUCKET_NAME,
                    Key=elem['Key']
                )


@app.get("/")
async def homepage():
    return {"Hello": "MW"}


@app.get("/weather")
async def weather(city: Union[str, None] = None):
    # first check in the s3 bucket, if the data exists, retrieve the latest
    # file and return the json data
    paginator = s3.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=S3_BUCKET_NAME, Prefix=city)
    latest = None
    for page in page_iterator:
        if "Contents" in page:
            latest2 = max(page['Contents'], key=lambda x: x['LastModified'])
            if latest is None or latest2['LastModified'] > latest['LastModified']:
                latest = latest2
    if latest:
        response = s3.get_object(Bucket=S3_BUCKET_NAME, Key=latest.get('Key'))
        content = response.get('Body')
        result = json.loads(content.read())
        return result
    else:
        # if no cached data found, we will make a call to the API and store the
        # data in the S3 bucket
        async with aiohttp.ClientSession() as session:
            city = city or 'Dhaka'
            weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}'
            async with session.get(weather_url) as response:
                result = await response.json()
                if response.status != 200:
                    raise HTTPException(status_code=404, detail=result)
                _now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
                file_name = f'{city}_{_now}.json'
                _upload = s3.put_object(Bucket=S3_BUCKET_NAME, Key=file_name, Body=json.dumps(result))

                # # DynamoDB logging
                # try:
                #     _res = dynamodb.put_item(
                #         TableName=DYNAMODB_TABLE_NAME,
                #         Item={
                #             'log_id': {'N': datetime.now().strftime('%s')},
                #             # 'key': {'S': file_name},
                #             'timestamp': {'S': _now},
                #             # 'path': {'S': f'{S3_BUCKET_NAME}/{file_name}'}
                #         }
                #     )
                #     print(_res)
                # except Exception as e:
                #     print(e)

                return result
