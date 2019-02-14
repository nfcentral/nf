NAME = "common"
PARENTS = []
FEATURES = []

FILES = {
    "": [("dotgitignore", ".gitignore"), ".nf/commands/build", ".nf/commands/up"]
}


EXAMPLE_FILES = {
}


def prepare(config, context):
    context.update({
        "gitignore": []
    })
