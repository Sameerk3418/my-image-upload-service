import json
import base64
import unittest
from unittest.mock import patch
import boto3
from moto import mock_s3
from download_thumbnail import lambda_handler

class TestDownloadThumbnail(unittest.TestCase):

    @mock_s3
    def setUp(self):
        self.s3 = boto3.client('s3')
        self.bucket_name = 'my-image-upload-bucket'
        self.s3.create_bucket(Bucket=self.bucket_name)

        # Upload a test thumbnail
        self.image_name = 'test_image.jpg'
        self.thumbnail_name = f'thumbnail_{self.image_name}'
        self.image_data = base64.b64encode(b'test_image_data').decode('utf-8')
        self.s3.put_object(Bucket=self.bucket_name, Key=self.thumbnail_name, Body=base64.b64decode(self.image_data))

    @mock_s3
    def test_download_thumbnail(self):
        event = {
            'pathParameters': {
                'imageName': self.thumbnail_name
            }
        }

        response = lambda_handler(event, None)

        # Validate response
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Content-Type', response['headers'])
        self.assertEqual(response['headers']['Content-Type'], 'image/jpeg')
        self.assertTrue(response['isBase64Encoded'])
        self.assertEqual(base64.b64decode(response['body']), b'test_image_data')

    def tearDown(self):
        pass  # Optional: Clean up resources if necessary

if __name__ == '__main__':
    unittest.main()
