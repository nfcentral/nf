import quart


app = quart.Quart("{{name}}")


@app.route("/")
async def index():
    return "Hello Satan\n"
