import json


NAME = "python/asgi"
PARENTS = ["python/base"]
FEATURES = []

FILES = {
}

EXAMPLE_FILES = {
}

LISTS = {
    "requirements_nf": {
        "": ["gunicorn",
             "uvicorn"]
    }
}

CONFIG_LISTS = {
}


def prepare(config, context):
    context.update({
        "app_run_command": json.dumps(["gunicorn", "{}:app".format(context["name"]), "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "-w", "1"]),
        "app_run_dev_command": json.dumps(["uvicorn", "--host", "0.0.0.0", "--port", "8000", "--debug", "{}:app".format(context["name"])])
    })
