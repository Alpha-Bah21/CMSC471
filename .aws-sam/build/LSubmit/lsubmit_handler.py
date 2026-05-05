import os
import boto3
import uuid
import json
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb')
sfn = boto3.client('stepfunctions')

def handler(event, context):
    body = json.loads(event['body'])
    file_name = body['filename']
    job_id = str(uuid.uuid4())
    
    job_table = os.environ['JOB_TABLE']
    table = dynamodb.Table(job_table)
    
    item = {
        'jobId': job_id,
        'status': 'RUNNING',
        'message': 'Job received, starting',
        'createdAt': datetime.now(timezone.utc).isoformat()
    }
    table.put_item(Item=item)
    
    state_machine_arn = os.environ['STATE_MACHINE_ARN']
    
    sfn.start_execution(
        stateMachineArn=state_machine_arn,
        name=job_id,
        input=json.dumps({
            'jobId': job_id,
            'filename': file_name
        })
    )
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*'
        },
        'body': job_id
    }