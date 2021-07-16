from settings import s3, db, S3_BUCKET_NAME, sns, TOPIC_ARN, sqs, QUEUE_URL
from aiohttp import web
from datetime import datetime


async def image_download(request):
    image_name = request.match_info.get('image')
    s3.download_file(S3_BUCKET_NAME, image_name, image_name)
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
    s3.upload_fileobj(image.file, S3_BUCKET_NAME, image.filename)
    sql = 'INSERT INTO metadata (name, modified_at, file_extension, size) ' \
          'VALUES (%s, %s, %s, %s)'
    val = (name, datetime.now(), extension, 6666)
    cursor = db.cursor()
    cursor.execute(sql, val)
    db.commit()
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        DelaySeconds=10,
        MessageAttributes={
            'name': {
                'DataType': 'String',
                'StringValue': name
            },
        },
        MessageBody=(
            'New image has been uploaded!'
        )
    )
    return web.json_response(status=201)


async def subscribe(request: web.Request):
    data = await request.json()
    response = sns.subscribe(
        TopicArn=TOPIC_ARN, Protocol="email", Endpoint=data['email']
    )
    return web.json_response(response, status=200)


async def unsubscribe(request: web.Request):
    data = await request.json()
    response = sns.list_subscriptions_by_topic(TopicArn=TOPIC_ARN)
    subscriptions = response["Subscriptions"]
    for sub in subscriptions:
        if sub['Endpoint'] == data['email']:
            response = sns.unsubscribe(SubscriptionArn=sub["SubscriptionArn"])
    return web.json_response(response, status=200)
