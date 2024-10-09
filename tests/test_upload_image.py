import json
import base64
import unittest
from unittest.mock import patch, MagicMock
import boto3
from moto import mock_s3, mock_sqs
from upload_image import lambda_handler

class TestUploadImage(unittest.TestCase):

    @mock_s3
    @mock_sqs
    def setUp(self):
        self.s3 = boto3.client('s3')
        self.sqs = boto3.client('sqs')
        self.bucket_name = 'my-image-upload-bucket'
        self.queue_name = 'thumbnailQueue'
        self.s3.create_bucket(Bucket=self.bucket_name)

        # Create an SQS queue
        self.queue_url = self.sqs.create_queue(QueueName=self.queue_name)['QueueUrl']

        # Set environment variables
        os.environ['IMAGE_BUCKET'] = self.bucket_name
        os.environ['THUMBNAIL_QUEUE_URL'] = self.queue_url

    @mock_s3
    @mock_sqs
    def test_upload_image(self):
        image_data = base64.b64encode(b'test_image_data').decode('utf-8')
        image_name = 'test_image.jpg'

        event = {
            'body': json.dumps({'image': image_data, 'name': image_name})
        }

        response = lambda_handler(event, None)

        # Validate response
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Image uploaded successfully', response['body'])

        # Check that the image was uploaded to S3
        s3_response = self.s3.get_object(Bucket=self.bucket_name, Key=image_name)
        self.assertIsNotNone(s3_response)

    def tearDown(self):
        pass  # Optional: Clean up resources if necessary

if __name__ == '__main__':
    unittest.main()
