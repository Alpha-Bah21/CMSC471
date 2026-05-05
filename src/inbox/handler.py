import json
import boto3
import os

s3 = boto3.client('s3')
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
        filename = body['filename']
        s3.put_object(Bucket=bucket, Key=filename, ContentType='image/png')
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(filename)
        }

    elif method == 'DELETE':
        key = event['pathParameters']['key']
        s3.delete_object(Bucket=bucket, Key=key)
        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"deleted": key})
        }