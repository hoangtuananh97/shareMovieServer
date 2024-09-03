import os
import time

import boto3
from botocore.exceptions import ClientError
from fastapi import HTTPException
from decouple import config

# S3 configuration
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_REGION = config("AWS_REGION")
S3_BUCKET = config("S3_BUCKET")

s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


def upload_file_to_s3(file, folder):
    try:
        filename, file_extension = os.path.splitext(file.filename)
        time_random = str(int(time.time()))
        file_name = f"{folder}/{filename}_{time_random}{file_extension}"
        s3_client.upload_fileobj(file.file, S3_BUCKET, file_name)
        return file_name
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")
