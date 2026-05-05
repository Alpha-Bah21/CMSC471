import json
import boto3
import os
from urllib.parse import unquote_plus
from botocore.config import Config

s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
bucket = os.environ['InboxBucketName']

def handler(event, context):
    method = event['httpMethod']

    if method == 'GET':
        response = s3.list_objects_v2(Bucket=bucket)
        files = [obj.get('Key') for obj in response.get('Contents', [])]
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(files)
        }

    elif method == 'POST':
        body = json.loads(event['body'])
        filename = body['file_name']
        url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': bucket,
                'Key': filename
            },
            ExpiresIn=300
        )
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"url": url})
        }

    elif method == 'DELETE':
        key = unquote_plus(event['pathParameters']['key'])
        s3.delete_object(Bucket=bucket, Key=key)
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"deleted": key})
        }