import json
import boto3
from openai import OpenAI

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

def get_parameter_value(key):
    ssm = boto3.client('ssm', 'eu-north-1')
    parameter = ssm.get_parameter(Name=key)
    return parameter['Parameter']['Value']


# Set up OpenAI API key
client = OpenAI(api_key=get_parameter_value("openAI-key"))

def handler(event, context):
    book_id = event["pathParameters"]["book-id"]
        
    dynamo_response = dynamodb.get_item(
        TableName='childrenbooks-dev',
        Key={'book-id': {'S': book_id}}
    )
    
    # Extract data from DynamoDB response
    if 'Item' in dynamo_response:
        item = dynamo_response['Item']
        # Access attributes from the item
        name = item.get('name', {}).get('S')
        gender = item.get('gender', {}).get('S')
        issue = item.get('issue', {}).get('S')
        value = item.get('value', {}).get('S')
        setting = item.get('setting', {}).get('S')
        
        # Send prompt to OpenAI
        MODEL = "gpt-3.5-turbo"
        response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You write small summaries of childrebook stories."},
            {"role": "user", "content": f"Bitte schreibe eine Geschichte über {name} einen {gender} wie er {issue} löst mit Hilfe von {value} in der Umgebung {setting}."},
        ],
        temperature=0,
        )
        
        # Return OpenAI response
        return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(response.choices[0].message.content)
        }
    else:
        return {
            'statusCode': 404,
            'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps('Item not found in DynamoDB')
        }        