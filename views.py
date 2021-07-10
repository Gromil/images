import os

import boto3
from aiohttp import web

client = boto3.client(
    's3',
    aws_access_key_id='',
    aws_secret_access_key='',
)
S3_URL = ''
S3_BUCKET_NAME = ''


async def image_download(request):
    image_name = request.match_info.get('image')
    client.download_file(S3_BUCKET_NAME, image_name, image_name)
    return web.FileResponse(image_name)


async def image_detail(request):
    # DB
    text = "Hello, "
    return web.Response(text=text)


async def image_create(request: web.Request):
    post = await request.post()
    image = post.get("image")
    client.upload_fileobj(image.file, S3_BUCKET_NAME, image.filename)
    return web.json_response(status=201)


async def image_delete(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def image_random_detail(request):
    # DB
    text = 'Hello'
    return web.Response(text=text)
