import boto3
import json
import uuid

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
            book_id = str(uuid.uuid4())
            request_body = json.loads(event['body'])
            selected_categories = request_body.get('categorySelectedOptionPairs', {})
            db_response = dynamodb.put_item(
                TableName='childrenbooks-dev',
                Item={
                    'book-id': {'S': book_id},
                    'gender': {'S': selected_categories["gender"]},
                    'name': {'S': selected_categories["name"]},
                    'value': {'S': selected_categories["value"]},
                    'issue': {'S': selected_categories["issue"]},
                }
            )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(book_id)
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