# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2022-09-19 15:59:40.657694
# @Last Modified by: CPS
# @Last Modified time: 2022-09-19 15:59:40.657694
# @file_path "W:\CPS\MyProject\python-tools\py-tool\core\mikepy"
# @Filename "xyz_to_shp.py"
# @Description: 功能描述
#
if __name__ == "__main__":
    import sys

    sys.path.append("..")
    sys.path.append("../../")

import os
from os import path

from pydantic import BaseModel
import geopandas as gpd


if __name__ == "__main__":
    shp_file = r"W:\CPS\MyProject\python-tools\py-tool\test\data\01_be_10.shp"
    xyz_file = r"W:\CPS\MyProject\python-tools\py-tool\static\upload\mikeio\res\10be_Current direction_1663315881.xyz"

    data = gpd.read_file(shp_file)

    print(data.crs)
