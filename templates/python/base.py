import os
import imp
import json
import click


NAME = "python/base"
PARENTS = ["common"]
FEATURES = ["jupyter",
            "jupyter_plots"]

FILES = {
    "": [".nf/commands/build",
         ".nf/commands/pipfreeze",
         ".nf/commands/up",
         ".nf/Dockerfile",
         ".nf/docker-compose.yml",
         ".nf/requirements.nf.txt",
         ".nf/requirements.nf.dev.txt",
         ".nf/.dir-locals.el",
         "common:.nf/ssh_host_ecdsa_key",
         "common:.nf/ssh_host_ecdsa_key.pub",
         "app/.nf/nf/__init__.py",
         "app/.nf/nf/config.py"]
}

EXAMPLE_FILES = {
    "": ["requirements.txt",
         "requirements.dev.txt",
         "nf.pipfreeze",
         "app/config.schema.json",
         "environment.dev.txt"]
}

LISTS = {
    "gitignore": {
        "": ["__pycache__"]
    },
    "requirements_nf_dev": {
        "jupyter": ["jupyterlab"],
        "jupyter_plots": ["matplotlib",
                          "seaborn"]
    },
    "dependencies_nf_dev_build": {
        "jupyter": ["libzmq3-dev"],
        "jupyter_plots": ["libpng-dev",
                          "libfreetype6-dev",
                          "libopenblas-dev"]
    },
    "dependencies_nf_dev": {
        "jupyter": ["libzmq3-dev"],
        "jupyter_plots": ["libpng16-16",
                          "libfreetype6",
                          "libopenblas-base"]
    }
}

CONFIG_LISTS = [
    "dependencies_build",
    "dependencies_dev_build",
    "dependencies",
    "dependencies_dev"
]


def prepare(config, context):
    nfconfig = imp.new_module("nfconfig")
    with open("/nf/templates/python/base/app/.nf/nf/config.py", "r") as f:
        exec(f.read(), nfconfig.__dict__)
    if os.path.exists("/project/app/config.schema.json"):
        with open("/project/app/config.schema.json", "r") as f:
            config_entries = nfconfig.parse(json.loads(f.read()))
    else:
        config_entries = []
    environment_dev = [{"_": "{}={}".format(c["name"].replace("{{NAME}}", config["name"].upper()), c["default"] if c["default"] is not None else "")} for c in config_entries]

    environment_dev_docker = []
    if os.path.exists("environment.dev.txt"):
        with open("environment.dev.txt", "r") as f:
            environment_dev_docker = [{"_": l.strip()} for l in f.readlines()]

    context.update({
        "python": {
            "version": config["python"],
            "version_short": ".".join(config["python"].split(".")[:2])
        },
        "environment_dev": environment_dev,
        "environment_dev_docker": environment_dev_docker
    })


def commands(cli):
    @cli.command()
    @click.option("--verbose/--no-verbose", default=False)
    def build(verbose):
        pass


    @cli.command()
    def up():
        pass


    @cli.command()
    def pipfreeze():
        pass
