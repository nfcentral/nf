import os
import json
import importlib
import pystache


with open("nf.json", "r") as f:
    config = json.loads(f.read())

template = importlib.import_module("templates.{}".format(config["template"]))
files, context = template.prepare(config)

for ((ff, ft), e) in files:
    ff = pystache.render(ff, context)
    ft = pystache.render(ft, context)
    if e and os.path.exists(ft):
        continue
    with open(ff) as f:
        content = pystache.render(f.read(), context)
    if os.path.dirname(ft) != "":
        os.makedirs(os.path.dirname(ft), exist_ok=True)
    with open(ft, "w") as f:
        f.write(content)
