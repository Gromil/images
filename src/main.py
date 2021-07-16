from aiohttp import web

from views import (
    image_create, image_detail, image_download, subscribe, unsubscribe
)

app = web.Application()
app.add_routes([
    web.post('/', image_create),
    web.post('/subscribe', subscribe),
    web.delete('/unsubscribe', unsubscribe),
    web.get('/{image}', image_detail),
    web.get('/{image}/download', image_download),
])

web.run_app(app)
