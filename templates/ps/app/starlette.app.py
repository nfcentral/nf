import starlette, starlette.applications, starlette.responses


app = starlette.applications.Starlette("{{name}}")


@app.route("/")
async def index(request):
    return starlette.responses.PlainTextResponse("Hello Satan\n")
