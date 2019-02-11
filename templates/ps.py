import os
import re


FEATURES = ["http", "http_aiohttp", "http_quart", "http_starlette", "jupyter", "jupyter_plots", "db", "db_postgres"]

REQUIREMENTS_NF = {
    "": ["uvloop"],
    "http_aiohttp": ["aiohttp", "gunicorn"],
    "http_quart": ["quart", "uvicorn"],
    "http_starlette": ["starlette", "uvicorn"],
    "db_postgres": ["psycopg2", "asyncpgsa"]
}

DEPENDENCIES_NF_BUILD = {
    "db_postgres": ["postgresql-dev"]
}

DEPENDENCIES_NF = {
    "db_postgres": ["libpq"]
}

REQUIREMENTS_NF_DEV = {
    "http_quart": ["hypercorn"],
    "http_starlette": ["hypercorn"],
    "jupyter": ["jupyterlab"],
    "jupyter_plots": ["pandas!=0.24.0,!=0.24.1", "matplotlib", "seaborn"]
}

DEPENDENCIES_NF_DEV_BUILD = {
    "jupyter": ["zeromq-dev"],
    "jupyter_plots": ["libpng-dev", "freetype-dev", "openblas-dev"]
}

DEPENDENCIES_NF_DEV = {
    "jupyter": ["zeromq-dev"],
    "jupyter_plots": ["libpng", "freetype", "openblas"]
}

FILES = {
    "": ["common:.nf/pipframer", ".nf/nf-release", ".nf/Dockerfile", ".nf/docker-compose.yml", "requirements.nf.txt", "requirements.nf.dev.txt", ".nf/.dir-locals.el"]
}

EXAMPLE_FILES = {
    "": ["common:.nf/ssh_host_ecdsa_key", "common:.nf/ssh_host_ecdsa_key.pub", ("_gitignore", ".gitignore"), "requirements.txt", "requirements.dev.txt"],
    "http_aiohttp": [("app/aiohttp.app.py", "app/{{name}}.py")],
    "http_quart": [("app/quart.app.py", "app/{{name}}.py")],
    "http_starlette": [("app/starlette.app.py", "app/{{name}}.py")]
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
            features.extend(["{}_{}".format(feature_split.group(1), option) for option in feature_split.group(2).split(",")])
        else:
            features.append(feature)

    for feature in FEATURES:
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
    files = [((os.path.join("..", *ff.split(":")), ft), e) if ":" in ff else ((ff, ft), e) for ((ff, ft), e) in files]
    files = [((ff, ft.split(":")[1]), e) if ":" in ft else ((ff, ft), e) for ((ff, ft), e) in files]
    files = [((os.path.join(root, ff), ft), e) for ((ff, ft), e) in files]

    return files, context
