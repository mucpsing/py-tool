# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2022-08-19 19:57:58.099895
# @Last Modified by: CPS
# @Last Modified time: 2022-08-19 19:57:58.099895
# @file_path "D:\CPS\MyProject\test"
# @Filename "yearbook_split.py"
# @Description: 检查完后，将abby处理后的结果进行导出，汇总所有数据到第一个sheet，同时根据站名也生成生成不同的sheet
#
import os, sys

sys.path.append("..")

from os import path
from pydantic import BaseModel
import pandas as pd

import cps_utils


def split_content(table):
    """
    将通过上一个main.py导出后的结果文件进行格式化

    - param table :{param} 通过pd.read_excel读取到的数据实例

    # 固定输出格式
    第一个sheet为汇总数据
    sheet名：站名
    ```markdown
    | 行            | 内容                                              |
    | ------------- | -------------------------------------------------|
    | 第一行（列名） | 月   日   时分  流量 (m3/s)   月   日   时分    |
    | 第二行（站名） | xxxxx站                                           |
    | 第三行（内容） | 真实的数据内容                                     |
    ```
    """
    region = []
    index = 0
    row_index = 0
    for row in table.itertuples(index=True):
        row_index += 1

        if not isinstance(row[1], str):
            continue

        if "start" in row[1]:
            region.append({"region": [row[0] + 1], "name": row[2]})

            if index != 0:
                region[index - 1]["region"].append(region[index]["region"][0] - 2)
            index += 1

    region[-1]["region"].append(row_index)

    return region


if __name__ == "__main__":
    # 2012_1660907093.xlsx
    cols_names = list(cps_utils.get_az("A", "T"))
    cols_show_names = ["月", "日", "时分", "水位 (m)", "流量 (m3/s)"] * 4
    target = path.realpath(r"./2015流量a_1660914198.xlsx")

    excel = pd.read_excel(
        target, names=cols_names, dtype="str", index_col=False, header=0
    )

    region = split_content(excel)

    writer = pd.ExcelWriter("./2015a_new.xlsx")
    excel.to_excel(writer, index=False, sheet_name="检查")

    for each in region:
        sheet_name = each["name"]

        header = pd.DataFrame([{"A": sheet_name}])
        content = excel[each["region"][0] : each["region"][1]]
        data = pd.concat([header, content])

        data.to_excel(
            writer, sheet_name=sheet_name, index=False, header=cols_show_names
        )

    writer.save()
