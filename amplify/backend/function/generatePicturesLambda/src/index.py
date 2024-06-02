import json
import boto3
import requests

def handler(event, context):

    response = requests.post(
    f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
    headers={
        "authorization": f"Bearer sk-d4L1y0TpKJH8VWuhykWzktsuNCHbIj14Wgm1P2kNH0jR86bt",
        "accept": "application/json"
    },
    files={"none": ''},
    data={
        "prompt": "character from a childbook",
        "output_format": "png",
    },
    )
 
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': response
    }
