from aiohttp import web

from views import (
    image_create, image_delete, image_detail, image_download,
    image_random_detail
)

app = web.Application()
app.add_routes([
    web.post('/', image_create),
    web.delete('/{image}', image_delete),
    web.get('/{image}', image_detail),
    web.get('/{image}/download', image_download),
    web.get('/random', image_random_detail),
])

web.run_app(app)
