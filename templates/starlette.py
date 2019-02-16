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
    pass
