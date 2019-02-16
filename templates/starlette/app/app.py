from starlette.applications import Starlette
from starlette.responses import UJSONResponse


app = Starlette("{{name}}")


@app.route("/")
async def index(request):
    return UJSONResponse({"answer": 42})
