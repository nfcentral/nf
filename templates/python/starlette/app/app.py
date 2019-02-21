from starlette.applications import Starlette
from starlette.responses import JSONResponse


app = Starlette("{{name}}")


@app.route("/")
async def index(request):
    return JSONResponse({"answer": 42})
