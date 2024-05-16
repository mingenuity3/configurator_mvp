import boto3
import json

dynamodb = boto3.client('dynamodb')

def handler(event, context):
    CallerMethod = event['httpMethod']
    ConstantGET = 'GET'
    ConstantPOST = 'POST'
    
    db_response = ""
    
    if CallerMethod == ConstantGET:
        BookId = event['pathParameters']['book-id']
        db_response = dynamodb.get_item(
            TableName='childrenbooks-dev',
            Key={
                'book-id': {
                    'S': BookId
                }
            }
            )
        
    if CallerMethod == ConstantPOST:
        BookId = event['pathParameters']['book-id']
        #Name = event['headers']['name']
        #Name = event['body'].get('name')
        ParsedJson = json.loads(event['body'])
        Name = ParsedJson['selectedOption']
        db_response = dynamodb.put_item(
            TableName='childrenbooks-dev',
            Item={
                'book-id': {
                    'S': BookId
                },
                'name': {
                    'S': Name
                }
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