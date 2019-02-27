import os
import sys
import re
import json
import importlib
import hashlib
import collections
import pystache
import click


class OrderedGroup(click.Group):
    def list_commands(self, ctx):
        return self.commands


with open("/nf/VERSION", "r") as f:
    VERSION = f.read()


if len(sys.argv) == 2 and sys.argv[1] == "nfinstall":
    with open("/nf/nf", "r") as f:
        print(f.read())
    exit()


if len(sys.argv) == 2 and sys.argv[1] == "nfcli":
    with open("/nf/nfcli", "r") as f:
        print(f.read())
    exit()


def templates_list(name):
    template = importlib.import_module("templates.{}".format(name.replace("/", ".")))
    templates = [template]
    for parent in template.PARENTS:
        templates.extend(templates_list(parent))
    return templates


def progress(ft, e, unmodified, action):
    print("[{}{}{}] {}".format("E" if e else ".", "." if unmodified else "M", action, ft))


@click.group(cls=OrderedGroup, commands=collections.OrderedDict())
def cli():
    pass


@cli.command()
def nfupgrade():
    pass


@cli.command()
def nffreeze():
    pass


@cli.command()
@click.argument("name")
def new(name):
    with open("/project/nf.json", "w") as f:
        f.write(json.dumps({
            "name": name,
            "template": "python/starlette",
            "python": "3.7.2",
            "features": []}, indent=4))


@cli.command()
def generate():
    with open("nf.json", "r") as f:
        config = json.loads(f.read())

    templates = templates_list(config["template"])
    templates.reverse()

    features = [""]
    for feature in config["features"]:
        feature_split = re.search("(.*)\[(.*)\]", feature)
        if feature_split is not None:
            features.append(feature_split.group(1))
            features.extend(["{}_{}".format(feature_split.group(1), option) for option in feature_split.group(2).split(",")])
        else:
            features.append(feature)
    config["features"] = features

    all_features = []
    for template in templates:
        all_features.extend(template.FEATURES)

    files = []
    context = {
        "name": config["name"],
        "features": {}
    }

    for feature in all_features:
        context["features"][feature] = feature in config["features"]

    for template in templates:
        template.prepare(config, context)
        tfiles = []
        for feature in config["features"]:
             tfiles.extend([(f, False) for f in template.FILES.get(feature, [])])
             tfiles.extend([(f, True) for f in template.EXAMPLE_FILES.get(feature, [])])
        tfiles = [(f, e) if isinstance(f, tuple) else ((f, f), e) for (f, e) in tfiles]
        tfiles = [((ff.replace(":", "/") if ":" in ff else "{}/{}".format(template.NAME, ff), ft), e) for ((ff, ft), e) in tfiles]
        tfiles = [((ff, ft.split(":")[1] if ":" in ft else ft), e) for ((ff, ft), e) in tfiles]
        files.extend(tfiles)

    all_lists = []
    for template in templates:
        for l in template.LISTS.keys():
            all_lists.append(l)
            if context.get(l) is None:
                context[l] = []
            for feature in features:
                context[l].extend([{"_": e} for e in template.LISTS[l].get(feature, [])])
        for l in template.CONFIG_LISTS:
            all_lists.append(l)
            if context.get(l) is None:
                context[l] = []
            context[l].extend([{"_": e} for e in config.get(l, [])])
    for l in set(all_lists):
        context["{}?".format(l)] = len(context[l]) != 0

    renderer = pystache.Renderer(escape=lambda u: u)
    root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
    generated = []
    tree = {}
    checksums = {}
    for ((ff, ft), e) in files:
        ff = os.path.join(root, renderer.render(ff, context))
        ft = pystache.render(ft, context)
        if not ft in tree:
            with open(ff) as f:
                content = renderer.render(f.read(), context)
            tree[ft] = content
            checksums[ft] = hashlib.md5(content.encode("utf-8")).hexdigest()
            generated.append((ft, e, checksums[ft]))

    generated_before = []
    if os.path.exists(".nf/generated.json"):
        with open(".nf/generated.json", "r") as f:
            generated_before = json.loads(f.read())

    checksums_before = {}
    checksums_real = {}
    for (ft, e, checksum) in generated_before:
        checksums_before[ft] = checksum
        if os.path.exists(ft):
            with open(ft, "r") as f:
                checksums_real[ft] = hashlib.md5(f.read().encode("utf-8")).hexdigest()

    generated_merged = []

    for (ft, e, checksum) in generated_before:
        if not ft in checksums:
            if not e or checksums_real.get(ft, None) == checksum:
                progress(ft, e, checksums_real.get(ft, None) == checksum, "D")
                os.unlink(ft)
            elif checksums_real.get(ft, None) is not None:
                progress(ft, e, checksums_real.get(ft, None) == checksum, "J")
                generated_merged.append((ft, e, checksum))
            else:
                pass

    for (ft, e, checksum) in generated:
        if os.path.dirname(ft) != "":
            os.makedirs(os.path.dirname(ft), exist_ok=True)
        if e and ft in checksums_real and checksums_real[ft] != checksums_before[ft]:
            progress(ft, e, checksums_real.get(ft, None) == checksums_before.get(ft, None), ".")
            generated_merged.append((ft, e, checksums_before[ft]))
            continue
        if not ft in checksums_real or checksums_real[ft] != checksums[ft]:
            progress(ft, e, checksums_real.get(ft, None) == checksums_before.get(ft, None), "G")
            with open(ft, "w") as f:
                f.write(tree[ft])
        else:
            progress(ft, e, checksums_real[ft] == checksums_before[ft], ".")
        generated_merged.append((ft, e, checksum))

    with open(".nf/generated.json", "w") as f:
        f.write(json.dumps(generated_merged))


if os.path.isfile("nf.json"):
    with open("nf.json", "r") as f:
        config = json.loads(f.read())
    templates = templates_list(config["template"])
    for template in templates:
        if "commands" in dir(template):
            template.commands(cli)

sys.argv[0] = "nf"
cli()
