import json
import boto3
import base64
import os

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

IMAGE_BUCKET = os.environ.get('IMAGE_BUCKET', 'my-image-upload-bucket')
THUMBNAIL_QUEUE_URL = os.environ.get('THUMBNAIL_QUEUE_URL')

def lambda_handler(event, context):
    body = json.loads(event['body'])
    image_data = body['image']  # Expecting base64 encoded image data
    image_name = body['name']     # Expecting image name

    # Decode and upload the image to S3
    image_bytes = base64.b64decode(image_data)
    s3.put_object(Bucket=IMAGE_BUCKET, Key=image_name, Body=image_bytes)

    # Send a message to SQS to generate the thumbnail
    sqs.send_message(
        QueueUrl=THUMBNAIL_QUEUE_URL,
        MessageBody=json.dumps({'image_name': image_name})
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Image uploaded successfully'})
    }
