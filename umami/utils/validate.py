_field_locs = ["field_1", "field_2", "field"]


def _validate_func(info, valid):
    # Function is defined
    if "_func" not in info:
        msg = "umami: The attribute, _func, is required for each calculation."
        raise ValueError(msg)

    # Function is supported
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
