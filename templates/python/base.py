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
         "common:.nf/ssh_host_ecdsa_key.pub"]
}

EXAMPLE_FILES = {
    "": ["requirements.txt",
         "requirements.dev.txt",
         "nf.pipfreeze"]
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
    context.update({
        "python": {
            "version": config["python"],
            "version_short": ".".join(config["python"].split(".")[:2])
        }
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
