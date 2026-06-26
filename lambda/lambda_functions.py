import json
import boto3
import os

def lambda_handler(event, context):

    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        file_name = record['s3']['object']['key']

        print(f"Bucket: {bucket_name}")
        print(f"File: {file_name}")

    # Get EC2 instance id from environment variable
    instance_id = os.environ['EC2_INSTANCE_ID']

    ec2 = boto3.client('ec2')
    ec2.start_instances(InstanceIds=[instance_id])

    return {
        'statusCode': 200,
        'body': json.dumps('ETL Trigger Successful')
    }