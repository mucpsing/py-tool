# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date:
# @Last Modified by: CPS
# @Last Modified time: 2021-10-28 23:50:31.856789
# @file_path "D:\CPS\MyProject\python-tools\mikepy"
# @Filename "mesh_to_shp.py"
# @Description: 功能描述
#
import geopandas as gpd
import os

import pandas as pd
from mikeio import Mesh, Dfsu
from os import path


def mike_file_to_shp(
    tar: str,
    output_name: str = None,
    *,
    item=0,
    setp: int = -1,
) -> str:
    """
    @Description 获取一个mike文件的外轮廓，保存为shp面文件

    - param tar         :{str} 支持格式：*.dfsu|*.mesh
    - param output_name :{str} 保存的shp文件名，如果不带后缀，则会自动创建文件夹

    returns `{type}` {description}
    @example
    ```py
    filename = r'./data/af2.dfsu'

    output_name = u'河道_面'

    res = to_shp(filename, output_name)

    if res:
        print('成功')

    ```

    """
    try:
        if not os.path.exists(tar):
            raise FileExistsError("文件不存在")

        if tar.endswith(".mesh"):
            data = Mesh(tar)[item][setp]
            dfs = pd.DataFrame({"data": data})
        elif tar.endswith(".dfsu"):
            dfs = Dfsu(tar)
        else:
            return ""

        # 如果不提供输出目录，则原地输出
        if not output_name:
            name, ext = path.splitext(os.path.basename(tar))
            output_path = os.path.abspath(os.path.dirname(tar))
            output_name = os.path.join(output_path, f"{name}.shp")

        shp = dfs.to_shapely()
        buffer = shp.buffer(0)

        gdf = gpd.GeoSeries([buffer])
        gdf.to_file(output_name)
        return output_name

    except Exception as e:
        print(f"发生错误了: {e}")
        return ""


if __name__ == "__main__":
    A = "./10be.dfsu"  # 工程前
    B = "./10af.dfsu"  # 工程后
    ITEMS_LIST = ["Current speed", "Current direction"]
    mike_file_to_shp(A, item=ITEMS_LIST[0])
