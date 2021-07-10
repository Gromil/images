from aiohttp import web

from views import (
    image_create, image_detail, image_download
)

app = web.Application()
app.add_routes([
    web.post('/', image_create),
    web.get('/{image}', image_detail),
    web.get('/{image}/download', image_download),
])

web.run_app(app)
