import os
import boto3

rds_data = boto3.client('rds-data')
dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    job_id = event['jobId']
    items = event['items']
    
    db_arn = os.environ['DB_ARN']
    secret_arn = os.environ['DB_SECRET']
    database = os.environ['DB_NAME']
    
    for item in items:
        rds_data.execute_statement(
            resourceArn=db_arn,
            secretArn=secret_arn,
            database=database,
            sql='INSERT INTO shopping_list (jobId, item) VALUES (:jobId, :item)',
            parameters=[
                {'name': 'jobId', 'value': {'stringValue': job_id}},
                {'name': 'item', 'value': {'stringValue': item}}
            ]
        )
        
    job_table = os.environ['JOB_TABLE']
    table = dynamodb.Table(job_table)
    
    table.update_item(
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