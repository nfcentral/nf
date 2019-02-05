import os
import re


REQUIREMENTS_NF = {
    "": ["uvloop"],
    "aiohttp": ["aiohttp", "gunicorn"],
    "quart": ["quart", "uvicorn"],
    "postgresql": ["psycopg2", "asyncpgsa"]
}

DEPENDENCIES_NF_BUILD = {
    "postgresql": ["postgresql-dev"]
}

DEPENDENCIES_NF = {
    "postgresql": ["libpq"]
}

REQUIREMENTS_NF_DEV = {
    "jupyter": ["jupyterlab"],
    "jupyter.plots": ["matplotlib", "seaborn"]
}

DEPENDENCIES_NF_DEV_BUILD = {
    "jupyter": ["zeromq-dev"]
}

DEPENDENCIES_NF_DEV = {
    "jupyter": ["zeromq-dev"]
}

FILES = {
    "": ["Dockerfile", "requirements.nf.txt", "requirements.nf.dev.txt"],
    "emacs": ["app/.dir-locals.el"]
}

EXAMPLE_FILES = {
    "": ["requirements.txt", "requirements.dev.txt"],
    "aiohttp": [("app/aiohttp.app.py", "app/{{name}}.py")],
    "quart": [("app/quart.app.py", "app/{{name}}.py")]
}


def prepare(config):
    context = {
        "name": config["name"],
        "python": {
            "version": config["python"],
            "version_short": ".".join(config["python"].split(".")[:2])
        },
        "requirements_nf": [],
        "requirements_nf_dev": [],
        "requirements": [],
        "requirements_dev": [],
        "dependencies_nf_build": [],
        "dependencies_build": [],
        "dependencies_nf_dev_build": [],
        "dependencies_dev_build": [],
        "dependencies": [],
        "dependencies_dev": [],
        "features": {}
    }

    features = [""]
    for feature in config["features"]:
        feature_split = re.search("(.*)\[(.*)\]", feature)
        if feature_split is not None:
            features.append(feature_split.group(1))
            features.extend(["{}.{}".format(feature_split.group(1), option) for option in feature_split.group(2).split(",")])
        else:
            features.append(feature)

    for feature in ["aiohttp", "quart", "jupyter", "jupyter.plots", "postgresql", "emacs"]:
        context["features"][feature] = feature in features

    extend_context = lambda sname, dname, source: context[dname].extend([{"_name": e} for e in source.get(sname, [])])
    files = []
    for feature in features:
        files.extend([(f, False) for f in FILES.get(feature, [])])
        files.extend([(f, True) for f in EXAMPLE_FILES.get(feature, [])])
        extend_context(feature, "requirements_nf", REQUIREMENTS_NF)
        extend_context(feature, "requirements_nf_dev", REQUIREMENTS_NF_DEV)
        extend_context(feature, "dependencies_nf_build", DEPENDENCIES_NF_BUILD)
        extend_context(feature, "dependencies_nf_dev_build", DEPENDENCIES_NF_DEV_BUILD)
        extend_context(feature, "dependencies", DEPENDENCIES_NF)
        extend_context(feature, "dependencies_dev", DEPENDENCIES_NF_DEV)
    extend_context("dependencies_build", "dependencies_build", config)
    extend_context("dependencies_dev_build", "dependencies_dev_build", config)
    extend_context("dependencies", "dependencies", config)
    extend_context("dependencies_dev", "dependencies_dev", config)

    root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ps")
    files = [(f, e) if isinstance(f, tuple) else ((f, f), e) for (f, e) in files]
    files = [((os.path.join(root, ff), ft), e) for ((ff, ft), e) in files]

    return files, context
