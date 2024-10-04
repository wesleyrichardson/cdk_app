import json
import boto3
from botocore.exceptions import ClientError

# Initialize S3 client
s3_client = boto3.client('s3')

# S3 bucket configuration
BUCKET_NAME = 'wesley-cdk-app-bucket'
S3_SUBFOLDER = 'data'

def process(file_name, file_content):
    """Upload file to S3 bucket"""
    try:
        s3_key = f"{S3_SUBFOLDER}/{file_name}"
        s3_client.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=file_content)
        print(f"File uploaded successfully: {s3_key}")
    except ClientError as e:
        print(f"Error uploading file to S3: {e}")
        raise

def lambda_handler(event, context):
    """Main Lambda handler function"""
    # Extract filename and content from the event body
    try:
        body = event['body']
        file_name = body.split('filename="')[1].split('"')[0]
        file_content = body.split('\r\n\r\n')[1].split('\r\n------')[0]

        # Process and upload the file
        process(file_name, file_content)

        # Prepare the response
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # IMPORTANT: Enable CORS for all origins
            },
            "body": json.dumps({
                "EventBody": "Success: your file has been uploaded and stored."
            })
        }

        return response
    except:
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"  # IMPORTANT: Enable CORS for all origins
            },
            "body": json.dumps({
                "EventBody": "Error: file upload not of correct format"
            })
        }
        return response
