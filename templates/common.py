NAME = "common"
PARENTS = []
FEATURES = []

FILES = {
    "": [("dotgitignore", ".gitignore")]
}


EXAMPLE_FILES = {
}


def prepare(config, context):
    context.update({
        "gitignore": []
    })
