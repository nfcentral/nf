NAME = "ps"
PARENTS = ["common"]
FEATURES = ["jupyter", "jupyter_plots", "postgres"]

FILES = {
    "": [".nf/commands/build", ".nf/commands/up", ".nf/pipframer", ".nf/Dockerfile", ".nf/docker-compose.yml", ".nf/requirements.nf.txt", ".nf/requirements.nf.dev.txt", ".nf/.dir-locals.el", "common:.nf/ssh_host_ecdsa_key", "common:.nf/ssh_host_ecdsa_key.pub"]
}

EXAMPLE_FILES = {
    "": ["requirements.txt", "requirements.dev.txt", ("app/app.py", "app/{{name}}.py")]
}

REQUIREMENTS_NF = {
    "": ["uvloop", "ujson", "starlette", "gunicorn", "uvicorn"],
    "postgres": ["psycopg2", "asyncpgsa"]
}

DEPENDENCIES_NF_BUILD = {
    "postgres": ["postgresql-dev"]
}

DEPENDENCIES_NF = {
    "postgres": ["libpq"]
}

REQUIREMENTS_NF_DEV = {
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


def prepare(config, context):
    context.update({
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
        "dependencies_dev": []
    })

    extend_rd = lambda source, sname, dname: context[dname].extend([{"_": e} for e in source.get(sname, [])])
    for feature in config["features"]:
        extend_rd(REQUIREMENTS_NF, feature, "requirements_nf")
        extend_rd(REQUIREMENTS_NF_DEV, feature, "requirements_nf_dev")
        extend_rd(DEPENDENCIES_NF_BUILD, feature, "dependencies_nf_build")
        extend_rd(DEPENDENCIES_NF_DEV_BUILD, feature, "dependencies_nf_dev_build")
        extend_rd(DEPENDENCIES_NF, feature, "dependencies")
        extend_rd(DEPENDENCIES_NF_DEV, feature, "dependencies_dev")
    extend_rd(config, "dependencies_build", "dependencies_build")
    extend_rd(config, "dependencies_dev_build", "dependencies_dev_build")
    extend_rd(config, "dependencies", "dependencies")
    extend_rd(config, "dependencies_dev", "dependencies_dev")
