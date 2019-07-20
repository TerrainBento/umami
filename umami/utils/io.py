from collections import OrderedDict
from io import StringIO

import yaml


def _read_input(file):
    if isinstance(file, StringIO):
        stream = file
    else:
        with open(file, "r") as f:
            stream = f.read()
    return OrderedDict(yaml.safe_load(stream))


def _write_output(out, stream):
    if isinstance(out, StringIO):
        f = out
        f.write(stream)
    else:
        with open(out, "w") as f:
            f.write(stream)
