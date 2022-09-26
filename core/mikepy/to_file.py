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

import time, enum
from os import path

import mikeio
import numpy as np

from typing import NewType
from pydantic import BaseModel
from pandas import DataFrame
import geopandas as gpd

CoordList = NewType("DataFrame[float]", list[float])

TXT = [".txt", ".xyz", ".csv"]
EXCEL = [".xls", ".xlsx"]
SHP = [".shp"]


class XY(BaseModel):
    x: CoordList
    y: CoordList


class OutType(str, enum.Enum):
    shp = ".shp"
    xls = ".xls"
    xlsx = ".xlsx"
    txt = ".txt"
    xyz = ".xyz"


class DataItem(str, enum.Enum):
    speed = "Current speed"
    direction = "Current direction"


def dfsu_to_file(
    dfsu_file: str,
    out_file: str = None,
    *,
    items: list[str | int] = None,
    setp: str | int = -1,
    exclude_value: list[int] = None,
) -> str:
    """
    解析dfsu，将指定的数据导出为shp文件

    - param dfsu_file :{str}                {description}
    - param out_file  :{str}                {description}
    - param items     :{list[str | int]}    {description}
    - param setp      :{str}                {description}

    @returns `{ str}` {description}

    """
    global TXT, EXCEL, SHP
    dir_path = path.dirname(dfsu_file)
    name, ext = path.splitext(path.basename(dfsu_file))
    try:
        dfs = mikeio.open(dfsu_file)
        xy = DataFrame(dfs.element_coordinates)

        # 当前不可用
        if not items:
            items = ["Current speed", "Current direction"]

        all_data = dfs.read(items=items, time=setp)
        z_speed = np.round(all_data[0].values, 3)
        z_direction_rad = np.round(all_data[1].values, 3)
        z_direction_angle = z_direction_rad * 180 / 3.14
        coords = dict()
        data = dict()

        # 根据exclude_value数据过滤数据
        if exclude_value:
            data["rad"] = []
            data["angle"] = []
            data["speed"] = []
            coords["x"] = []
            coords["y"] = []

            for index in range(0, len(z_direction_rad)):
                if int(z_direction_angle[index]) in exclude_value:
                    continue

                coords["x"].append(xy[0][index])
                coords["y"].append(xy[1][index])
                data["rad"].append(z_direction_rad[index])
                data["angle"].append(z_direction_angle[index])  # 如果是流向，将弧度转换为角度
                data["speed"].append(z_speed[index])
        else:
            coords = {"x": xy[0], "y": xy[1]}
            data["speed"] = z_speed
            data["angle"] = z_direction_rad
            data["speed"] = z_speed

        df = DataFrame(data)

        # 默认的输出shp文件
        if not out_file:
            out_file = path.join(
                dir_path, f"{name}_{int(time.time())}.shp".replace(" ", "_")
            )

        # txt
        out_name, out_ext = path.splitext(path.basename(out_file))
        if out_ext in TXT:
            df.to_csv(out_file, sep="\t", index=False, header=False)

        # excel
        elif out_ext in EXCEL:
            df.to_excel(out_file, index=False)

        # shp
        elif out_ext in SHP:
            gpd.GeoDataFrame(
                data, geometry=gpd.points_from_xy(coords["x"], coords["y"])
            ).to_file(out_file)

        return out_file

    except Exception as e:
        print("dfsu_to_file fail: ", e)
        return ""


if __name__ == "__main__":
    A = "./10be.dfsu"  # 工程前
    B = "./10af.dfsu"  # 工程后
    T = r"W:\CPS\MyProject\python-tools\py-tool\static\upload\mikeio\1.dfsu"

    ITEMS_LIST = [DataItem.speed, DataItem.direction]
    # dfsu_to_file(A, item=ITEMS_LIST[0])
    res = dfsu_to_file(T, out_file="./B.shp", exclude_value=[0, 360])
    print("res: ", res)
