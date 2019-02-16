import json


NAME = "starlette"
PARENTS = ["asgi"]
FEATURES = []

FILES = {
}

EXAMPLE_FILES = {
    "": [("app/app.py", "app/{{name}}.py")]
}

LISTS = {
    "requirements_nf": {
        "": ["starlette"]
    }
}

CONFIG_LISTS = {
}


def prepare(config, context):
    context.update({
        "app_run_command": json.dumps(["gunicorn", "{}:app".format(context["name"]), "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "-w", "1"]),
        "app_run_dev_command": json.dumps(["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--debug", "{}:app".format(context["name"])])
    })
