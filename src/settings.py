import os

import boto3
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

S3_URL = os.environ.get("S3_URL")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

TOPIC_ARN = os.environ.get("TOPIC_ARN")

QUEUE_URL = os.environ.get("QUEUE_URL")

s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
sns = boto3.client(
    'sns',
    region_name='us-east-2',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
sqs = boto3.client(
    'sqs',
    region_name='us-east-2',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS images")
db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database='images'
)
cursor = db.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS metadata("
    "name VARCHAR(255), "
    "modified_at VARCHAR(255),"
    "file_extension VARCHAR(255),"
    "size INTEGER(255)"
    ")"
)
