from settings import client, db, S3_BUCKET_NAME
from aiohttp import web
from datetime import datetime


async def image_download(request):
    image_name = request.match_info.get('image')
    client.download_file(S3_BUCKET_NAME, image_name, image_name)
    return web.FileResponse(image_name)


async def image_detail(request):
    image_name = request.match_info.get('image')
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM metadata Where name = "{image_name}"')
    images = cursor.fetchall()
    data = [
        {
            'name': image[0], 'modified_at': image[1],
            'file_extension': image[2], 'size': image[3]
        }
        for image in images
    ]
    return web.json_response(data, status=200)


async def image_create(request: web.Request):
    post = await request.post()
    image = post.get("image")
    image_name = image.filename.split('.')
    name, extension = image_name[0], image_name[1]
    client.upload_fileobj(image.file, S3_BUCKET_NAME, image.filename)
    sql = 'INSERT INTO metadata (name, modified_at, file_extension, size) ' \
          'VALUES (%s, %s, %s, %s)'
    val = (name, datetime.now(), extension, 6666)
    cursor = db.cursor()
    cursor.execute(sql, val)
    db.commit()
    return web.json_response(status=201)


async def subscribe(request: web.Request):
    data = await request.json()
    sql = 'INSERT INTO subscription (email) VALUES (%s)'
    val = (data['email'],)
    cursor = db.cursor()
    cursor.execute(sql, val)
    db.commit()
    return web.json_response(status=200)


async def unsubscribe(request: web.Request):
    data = await request.json()
    sql = "DELETE FROM subscription WHERE email = %s"
    value = (data['email'],)
    cursor = db.cursor()
    cursor.execute(sql, value)
    db.commit()
    return web.json_response(status=200)
