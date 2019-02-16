import os
import re
import json
import importlib
import pystache


def templates_list(name):
    template = importlib.import_module("templates.{}".format(name))
    templates = [template]
    for parent in template.PARENTS:
        templates.extend(templates_list(parent))
    return templates


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

    for template in templates:
        for l in template.LISTS.keys():
            if context.get(l) is None:
                context[l] = []
            for feature in features:
                context[l].extend([{"_": e} for e in template.LISTS[l].get(feature, [])])
        for l in template.CONFIG_LISTS:
            if context.get(l) is None:
                context[l] = []
            context[l].extend([{"_": e} for e in config.get(l, [])])

    root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
    for ((ff, ft), e) in files:
        ff = os.path.join(root, pystache.render(ff, context))
        ft = pystache.render(ft, context)
        if e and os.path.exists(ft):
            continue
        with open(ff) as f:
            content = pystache.render(f.read(), context)
        if os.path.dirname(ft) != "":
            os.makedirs(os.path.dirname(ft), exist_ok=True)
        with open(ft, "w") as f:
            f.write(content)


generate()
