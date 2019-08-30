_field_locs = ["field_1", "field_2", "field"]


def _validate_func(key, info, valid):
    # Is function defined?
    if "_func" not in info:
        msg = (
            "umami: The attribute _func, is required for each calculation. "
            "missing for {key}."
        ).format(key=key)
        raise ValueError(msg)

    # Is function supported?
    func = info["_func"]
    if func not in valid:
        msg = "umami: The value passed for _func is not valid."
        raise ValueError(msg)


def _validate_fields(grid, info):
    for fl in _field_locs:
        if fl in info:
            if info[fl] not in grid.at_node:
                msg = ""
                raise ValueError(msg)
