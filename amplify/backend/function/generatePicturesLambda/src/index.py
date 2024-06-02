import json
import boto3
import requests
import base64

def handler(event, context):

    response = requests.post(
    f"https://api.stability.ai/v2beta/stable-image/generate/sd3",
    headers={
        "authorization": f"Bearer sk-d4L1y0TpKJH8VWuhykWzktsuNCHbIj14Wgm1P2kNH0jR86bt",
        "accept": "image/*"
    },
    files={"none": ''},
    data={
        "prompt": "character from a childbook",
        "output_format": "jpeg",
    },
    )
    #image_data_encoded = response.json()["image"]
    #image_data = base64.b64decode(image_data_encoded)
 
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Content-Type': 'image/jpeg'
        },
        'body': json.dumps(response.content)
    }
