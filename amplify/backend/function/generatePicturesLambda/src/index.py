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
    img = response.content
    #print(type(img))                      # Just getting type.
    myObj = [base64.b64encode(img)]          # Encoded the image to base64
    #print(type(myObj))            # Printing the values
    #print(myObj[0])               # get the base64 format of the image
    #print('type(myObj[0]) ================>',type(myObj[0]))
    return_json = str(myObj[0])           # Assing to return_json variable to return.
    #print('return_json ========================>',return_json)
    return_json = return_json.replace("b'","")          # replace this 'b'' is must to get absoulate image.
    encoded_image = return_json.replace("'","")
 
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
            'Content-Type': 'image/jpeg'
        },
        'encoded_image': encoded_image
    }
