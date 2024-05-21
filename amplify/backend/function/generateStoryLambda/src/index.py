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
        TableName='childrensbooks-dev',
        Key={'book-id': {'S': book_id}}
    )
    
    # Extract data from DynamoDB response
    if 'Item' in dynamo_response:
        entry = dynamo_response['Item']
        # Assuming you have an attribute named 'data' in DynamoDB that contains the information you want to send to OpenAI
        # data_to_send = entry['issue']['S']
        
        # Send prompt to OpenAI
        MODEL = "gpt-3.5-turbo"
        response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You write small summaries of childrebook stories."},
            {"role": "user", "content": "Bitte schreibe eine Geschichte über Gordon & seine Abenteuer."},
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