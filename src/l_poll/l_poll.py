import os
import boto3
import json

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    job_id = event['pathParameters']['jobId']
    
    table_name = os.environ['JOB_TABLE']
    table = dynamodb.Table(table_name)
    
    result = table.get_item(Key={'jobId': job_id})
    item = result.get('Item', {})
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'jobId': item.get('jobId', job_id),
            'status': item.get('status', 'unknown'),
            'message': item.get('message', '...')
        })
    }