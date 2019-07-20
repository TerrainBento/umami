_field_locs = ["field_1", "field_2", "field"]


def _validate_func(info, valid):
    # Function is defined
    if "_func" not in info:
        msg = ""
        raise ValueError(msg)

    # Function is supported
    func = info["_func"]
    if func not in valid:
        msg = ""
        raise ValueError(msg)


def _validate_fields(grid, info):
    for fl in _field_locs:
        if fl in info:
            if info[fl] not in grid.at_node:
                msg = ""
                raise ValueError(msg)
