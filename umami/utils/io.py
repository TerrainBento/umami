
import yaml
from collections import OrderedDict
from io import StringIO


def _read_input(file):
    if isinstance(file, (str, StringIO)):
        stream = file
    else:
        with open(file, "r") as f:
            stream = f.readlines()
    return OrderedDict(yaml.safe_load(stream))
