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

client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
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

cursor.execute('''
    CREATE TABLE IF NOT EXISTS subscription(
    email VARCHAR(255)
    )
    '''
)
