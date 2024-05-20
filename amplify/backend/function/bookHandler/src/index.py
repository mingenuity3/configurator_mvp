import boto3
import json

dynamodb = boto3.client('dynamodb')

def handler(event, context):
    caller_method = event['httpMethod']
    constant_get = 'GET'
    constant_post = 'POST'
    
    try:
        if caller_method == constant_get:
            book_id = event['pathParameters'].get('book-id', '')
            db_response = dynamodb.get_item(
                TableName='childrenbooks-dev',
                Key={
                    'book-id': {'S': book_id}
                }
            )
            
        elif caller_method == constant_post:
            book_id = event['pathParameters'].get('book-id', '')
            body = json.loads(event['body'])
            name = body.get('selectedOption', '')
            db_response = dynamodb.put_item(
                TableName='childrenbooks-dev',
                Item={
                    'book-id': {'S': book_id},
                    'name': {'S': name}
                }
            )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(db_response)
        }
    
    except Exception as e:
        # Handle any exceptions
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'error': str(e)})
        }