from collections import OrderedDict

relative_xy_template = {
    "left_top": [0, 0],
    "right_top": [1, 1],
    "right_down": [2, 2],
    "left_down": [3, 3],
}

list_xy = OrderedDict(relative_xy_template)
print(tuple(relative_xy_template.values()))
