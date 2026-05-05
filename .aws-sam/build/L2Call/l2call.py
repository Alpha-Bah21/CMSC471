import os
import boto3

textract = boto3.client('textract')
dynamodb = boto3.resource('dynamodb')

def handler(event, context):
    job_id = event['jobId']
    file_name = event['filename']
    bucket = event['bucket']
    
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket,
                'Name': file_name
            }
        }
    )
    
    items = []
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            items.append(block['Text'])
            
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
            ':s': 'PROCESSING',
            ':m': 'Textract completed'
        }
    )
    
    return {
        'jobId': job_id,
        'items': items
    }