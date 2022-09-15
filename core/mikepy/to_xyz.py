# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2022-09-13 14:58:25.831843
# @Last Modified by: CPS
# @Last Modified time: 2022-09-13 14:58:25.831843
# @file_path "W:\CPS\MyProject\test"
# @Filename "dsfu_to_xy.py"
# @Description: 功能描述
#
if __name__ == "__main__":
    import sys

    sys.path.append("..")
    sys.path.append("../../")

import os, time
from os import path

import mikeio
import numpy as np

from typing import NewType
from pydantic import BaseModel
from pandas import DataFrame
from mikeio import Dfsu, Mesh

CoordList = NewType("DataFrame[float]", list[float])


class XY(BaseModel):
    x: CoordList
    y: CoordList


# def dfsu_to_xy(dfsu_file: str, out_file: str = None) -> str:
#     dir_path = path.dirname(dfsu_file)
#     name, ext = path.splitext(path.basename(dfsu_file))

#     if ext == ".mesh":
#         dfs = Mesh(dfsu_file)
#     elif ext == ".dfsu":
#         dfs = Dfsu(dfsu_file)
#     else:
#         return False

#     if not out_file:
#         out_file = path.join(dir_path, f"{name}_xy_{int(time.time())}.txt")

#     xyz = DataFrame(dfs.element_coordinates)
#     res = {"x": xyz[0], "y": xyz[1]}

#     df = DataFrame(data=res)

#     df.to_csv(f"{name}_xy_{int(time.time())}.txt", sep="\t", index=False, header=False)
#     df.to_excel(f"{name}_xy_{int(time.time())}.xls", index=False)
#     df.to_excel(f"{name}_xy_{int(time.time())}.xlsx", index=False)

#     return out_file


def dfsu_to_xyz(
    dfsu_file: str, out_file: str = None, *, item: int | str = 0, setp: str | int = -1
) -> str:
    dir_path = path.dirname(dfsu_file)
    name, ext = path.splitext(path.basename(dfsu_file))

    dfs = mikeio.open(dfsu_file)
    xy = DataFrame(dfs.element_coordinates)
    z = dfs.read(items=[item], time=setp)[0]

    df = DataFrame(data={"x": xy[0], "y": xy[1], "z": np.round(z.values, 3)})

    if not out_file:
        out_file = path.join(
            dir_path, f"{name}_{item}_{int(time.time())}.txt".replace(" ", "_")
        )

    df.to_csv(out_file, sep="\t", index=False, header=False)

    return


if __name__ == "__main__":
    A = "./10be.dfsu"  # 工程前
    B = "./10af.dfsu"  # 工程后
    ITEMS_LIST = ["Current speed", "Current direction"]
    dfsu_to_xyz(A, item=ITEMS_LIST[0])
