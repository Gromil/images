from settings import sqs, sns, QUEUE_URL, TOPIC_ARN, db


def send_to_subs():
    response = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    messages = response['Messages']
    for message in messages:
        text = get_email_text(
            message['MessageAttributes']['name']['StringValue']
        )
        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=text,
            Subject="New Image"
        )


def get_email_text(image_name):
    image_url = f'http://localhost:8080/{image_name}/download'
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM metadata Where name = "{image_name}"')
    image = cursor.fetchone()
    return f'Image with name {image[0]}.{image[2]} with size {image[3]} ' \
           f'was uploaded at {image[1]}.' \
           f'You can download it at {image_url}'
