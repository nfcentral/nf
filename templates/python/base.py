NAME = "python/base"
PARENTS = ["common"]
FEATURES = ["freeze",
            "jupyter",
            "jupyter_plots",
            "postgres"]

FILES = {
    "": [".nf/commands/build",
         ".nf/commands/up",
         ".nf/pipframer",
         ".nf/Dockerfile",
         ".nf/docker-compose.yml",
         ".nf/requirements.nf.txt",
         ".nf/requirements.nf.dev.txt",
         ".nf/.dir-locals.el",
         "common:.nf/ssh_host_ecdsa_key",
         "common:.nf/ssh_host_ecdsa_key.pub"]
}

EXAMPLE_FILES = {
    "": ["requirements.txt",
         "requirements.dev.txt"],
    "freeze": ["nf.pipfreeze"]
}

LISTS = {
    "gitignore": {
        "": ["__pycache__"]
    },
    "requirements_nf": {
        "": ["uvloop",
             "ujson"],
        "postgres": ["psycopg2",
                     "asyncpgsa"]
    },
    "dependencies_nf_build": {
        "postgres": ["postgresql-dev"]
    },
    "dependencies_nf": {
        "postgres": ["libpq"]
    },
    "requirements_nf_dev": {
        "jupyter": ["jupyterlab"],
        "jupyter_plots": ["pandas!=0.24.0,!=0.24.1",
                          "matplotlib",
                          "seaborn"]
    },
    "dependencies_nf_dev_build": {
        "jupyter": ["zeromq-dev"],
        "jupyter_plots": ["libpng-dev",
                          "freetype-dev",
                          "openblas-dev"]
    },
    "dependencies_nf_dev": {
        "jupyter": ["libzmq"],
        "jupyter_plots": ["libpng",
                          "freetype",
                          "openblas"]
    }
}

CONFIG_LISTS = [
    "dependencies_build",
    "dependencies_dev_build",
    "dependencies",
    "dependencies_dev"
]


def prepare(config, context):
    context.update({
        "python": {
            "version": config["python"],
            "version_short": ".".join(config["python"].split(".")[:2])
        }
    })
