import nf
from starlette.applications import Starlette
from starlette.responses import JSONResponse


config = nf.config.get()
app = Starlette("{{name}}")


@app.route("/")
async def index(request):
    return JSONResponse({"answer": 42})
