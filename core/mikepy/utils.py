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

from mikeio import Mesh, Dfsu


def mike_file_to_shp(tar: str, output_name: str = None) -> str:
    """
    @Description 获取一个mike文件的外轮廓，保存为shp面文件

    - param tar         :{str} 支持格式：*.dfsu|*.mesh
    - param output_name :{str} 保存的shp文件名，不需要带后缀

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

        if tar.endswith(".dfsu"):
            dfs = Dfsu(tar)
        elif tar.endswith(".mesh"):
            dfs = Mesh(tar)
        else:
            return ""

        if output_name:
            name, ext = os.path.basename(tar).split(".")
            base_path = os.path.abspath(os.path.dirname(tar))
            name = output_name
            output_name = os.path.join(base_path, f"{name}.shp")

        shp = dfs.to_shapely()
        buffer = shp.buffer(0)

        gdf = gpd.GeoSeries([buffer])
        gdf.to_file(output_name)
        return output_name

    except Exception as e:
        print(f"发生错误了: {e}")
        return ""


if __name__ == "__main__":
    filename = r"./data/af2.dfsu"

    res = mike_file_to_shp(filename)

    if res:
        print("成功")
