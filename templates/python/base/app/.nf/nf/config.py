import os
import json


def _parse_value(value, schema):
    if schema["type"] == "string":
        return (value, True)
    if schema["type"] == "number":
        try:
            return (int(value), True)
        except:
            try:
                return (float(value), True)
            except:
                return (value, False)
    if schema["type"] == "boolean":
        if value == "true":
            return (True, True)
        if value == "false":
            return (False, True)
        return (value, False)
    if schema["type"] == "array":
        item_type = schema["items"]["type"]
        value = value.split(",")
        value = [_parse_value(v, {"type": item_type}) for v in value]
        return ([v[0] for v in value], any(v[1] == False for v in value))
    return (value, False)


def _set_config_value(config, path, value):
    if len(path) == 1:
        config[path[0]] = value
        return
    if config.get(path[0]) is None:
        config[path[0]] = {}
    _set_config_value(config[path[0]], path[1:], value)


def _to_dict(config_list):
    config = {}
    for e in config_list:
        _set_config_value(config, e["path"], e["value"])
    return config


def parse(schema, required=False, path=[]):
    if schema["type"] == "object":
        result = []
        for name in schema["properties"].keys():
            result.extend(parse(schema["properties"][name],
                                 required or ("required" in schema and name in schema["required"]),
                                 path + [name]))
        return result
    name = ("_".join(["{{name}}"] + path)).upper()
    default = schema.get("default", None)
    (value, valid) = _parse_value(os.environ.get(name, default), schema)
    return [{"name": name,
             "path": path,
             "type": schema["type"],
             "required": required,
             "default": default,
             "value": value,
             "valid": valid,
             "description": schema.get("description", None)}]


def get():
    with open("config.schema.json", "r") as f:
        config_list = parse(json.loads(f.read()))
    return _to_dict(config_list)
