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
    request_body = json.loads(event['body'])
    name = request_body.get('name')
    gender = request_body.get('gender')
    issue = request_body.get('issue')
    value = request_body.get('value')
    
    # Send prompt to OpenAI
    MODEL = "gpt-3.5-turbo"
    response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "You assist in creating possible answers to questions that help getting feedback from a user to create a childrebook stories."},
        {"role": "user", "content": f"Generiere drei Antwortmöglichkeiten bestehend aus jeweils einem Wort zur Frage Wo spielt die Geschichte geografisch? basieren auf den bisherigen Eingaben des Kunden: Name {name}, Geschlecht {gender}, Problem {issue}, Werte der Geschichte {value}."},
    ],
    temperature=0,
    )

    lines = str.splitlines(response.choices[0].message.content)
    output = [line.split('. ')[1].strip() for line in lines]

    print(output)
  
    return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      },
      'body': json.dumps(output)
    }
