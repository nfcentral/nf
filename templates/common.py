NAME = "common"
PARENTS = []
FEATURES = []

FILES = {
    "": [("dotgitignore", ".gitignore")]
}

EXAMPLE_FILES = {
}

LISTS = {
}

CONFIG_LISTS = {
}


def prepare(config, context):
    context.update({
        "gitignore": []
    })
