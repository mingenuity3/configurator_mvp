import json
import boto3
import openai

# Initialize DynamoDB client
dynamodb = boto3.client('dynamodb')

def get_parameter_value(key):
    ssm = boto3.client('ssm', 'eu-central-1')
    parameter = ssm.get_parameter(Name=key)
    return parameter['Parameter']['Value']


# Set up OpenAI API key
openai.api_key = get_parameter_value("openAI-key")

def lambda_handler(event, context):
    request_body = json.loads(event['body'])
    bookid = request_body.get('bookid', {})
    # Retrieve entry from DynamoDB
    dynamo_response = dynamodb.get_item(
        TableName='childrensbooks-dev',
        Key={'id': {'S': bookid}}
    )
    
    # Extract data from DynamoDB response
    if 'Item' in dynamo_response:
        entry = dynamo_response['Item']
        # Assuming you have an attribute named 'data' in DynamoDB that contains the information you want to send to OpenAI
        data_to_send = entry['issue']['S']
        
        # Send prompt to OpenAI
        response = openai.Completion.create(
            engine="text-davinci-002",  # Specify the engine you want to use
            prompt=data_to_send,
            max_tokens=50  # Specify the maximum number of tokens for the completion
        )
        
        # Return OpenAI response
        return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(response.choices[0].text)  # Assuming you want to return the text generated by OpenAI
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


