import os
import boto3
import uuid
import json
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    job_id = event['jobId']
    items = event['items']
    
    records_table = dynamodb.Table(os.environ['RECORDS_TABLE'])
    job_table = dynamodb.Table(os.environ['JOB_TABLE'])
    
    for item in items:
        record = {
            'id': str(uuid.uuid4()),
            'job_id': job_id,
            'item': item,
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        records_table.put_item(Item=record)
    
    job_table.update_item(
        Key={'jobId': job_id},
        UpdateExpression='SET #s = :s, #m = :m',
        ExpressionAttributeNames={
            '#s': 'status',
            '#m': 'message'
        },
        ExpressionAttributeValues={
            ':s': 'SUCCEEDED',
            ':m': 'Saved'
        }
    )
    
    return {
        'jobId': job_id,
        'rowCount': len(items)
    }