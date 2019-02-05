from aiohttp import web


routes = web.RouteTableDef()


@routes.get("/")
async def index(request):
    return web.Response(text="Hello Satan\n")


async def app():
    app = web.Application()
    app.add_routes(routes)
    return app
