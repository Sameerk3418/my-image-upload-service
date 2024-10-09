import json
import base64
import boto3
import os

s3 = boto3.client('s3')

IMAGE_BUCKET = os.environ.get('IMAGE_BUCKET', 'my-image-upload-bucket')

def lambda_handler(event, context):
    image_name = event['pathParameters']['imageName']
    response = s3.get_object(Bucket=IMAGE_BUCKET, Key=image_name)
    image_body = response['Body'].read()

    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'image/jpeg'},
        'body': base64.b64encode(image_body).decode('utf-8'),
        'isBase64Encoded': True
    }
