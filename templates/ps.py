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

    files = []
    for feature in features:
        files.extend([(f, False) for f in FILES.get(feature, [])])
        files.extend([(f, True) for f in EXAMPLE_FILES.get(feature, [])])
        context["requirements_nf"].extend([{"_name": r} for r in REQUIREMENTS_NF.get(feature, [])])
        context["requirements_nf_dev"].extend([{"_name": r} for r in REQUIREMENTS_NF_DEV.get(feature, [])])
        context["dependencies_nf_build"].extend([{"_name": d} for d in DEPENDENCIES_NF_BUILD.get(feature, [])])
        context["dependencies_nf_dev_build"].extend([{"_name": d} for d in DEPENDENCIES_NF_DEV_BUILD.get(feature, [])])
        context["dependencies"].extend([{"_name": d} for d in DEPENDENCIES_NF.get(feature, [])])
        context["dependencies_dev"].extend([{"_name": d} for d in DEPENDENCIES_NF_DEV.get(feature, [])])
    context["dependencies_build"].extend([{"_name": d} for d in config.get("dependencies_build", [])])
    context["dependencies_dev_build"].extend([{"_name": d} for d in config.get("dependencies_dev_build", [])])
    context["dependencies"].extend([{"_name": d} for d in config.get("dependencies", [])])
    context["dependencies_dev"].extend([{"_name": d} for d in config.get("dependencies_dev", [])])

    root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ps")
    files = [(f, e) if isinstance(f, tuple) else ((f, f), e) for (f, e) in files]
    files = [((os.path.join(root, ff), ft), e) for ((ff, ft), e) in files]

    return files, context
