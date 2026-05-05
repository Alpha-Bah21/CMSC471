import os
import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['RECORDS_TABLE'])

def handler(event, context):
    method = event['httpMethod']
    
    if method == 'GET':
        rows = get_records()
        print(json.dumps(rows))
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(rows)
        }
    
    elif method == 'DELETE':
        record_id = event['pathParameters']['id']
        delete_record(record_id)
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'deleted': record_id})
        }

def get_records():
    result = table.scan()
    rows = []
    
    for r in result.get('Items', []):
        rows.append({
            'id': r.get('id'),
            'item': r.get('item'),
            'created_at': r.get('created_at', '')
        })
        
    rows.sort(key=lambda x: x['created_at'])
    return rows

def delete_record(record_id):
    table.delete_item(Key={'id': record_id})
    