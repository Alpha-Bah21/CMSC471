import os
import boto3

s3 = boto3.client('s3')

def handler(event, context):
    job_id = event['jobId']
    file_name = event['filename']
    bucket = os.environ['BUCKET_NAME']
    
    s3.get_object(Bucket=bucket, Key=file_name)
    
    return {
        'jobId': job_id,
        'filename': file_name,
        'bucket': bucket
    }