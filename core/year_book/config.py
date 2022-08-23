# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date:
# @Last Modified by: CPS
# @Last Modified time: 2022-08-23 11:29:48.160094
# @file_path "W:\CPS\MyProject\python-tools\py-tool\core\year_book"
# @Filename "config.py"
# @Description: 功能描述
#
if __name__ == "__main__":
    import sys

    sys.path.append("..")
    sys.path.append("../../")

import os
from os import path

from pydantic import BaseModel
from typing import TypeAlias

from utils import index as cps_utils

STATION_NAMES = [
    "小古箓站",
    "飞来峡站",
    "石角站",
    "坪石（二）站",
    "犁市（二）站",
    "滃江站",
    "高道站",
    "珠坑站",
]

WordColReplaceNames: TypeAlias = str


class ABBYYearBookExcelFilterSettings(BaseModel):
    fix_24_to_new_day: bool = True  # 部分年鉴会使用24作为小时单位，修复后改位置变成0，日数据添加1
    fix_24_col_names: list[str] = ["C", "H", "M", "R"]
    word_strip: str  # 一些在数据前后的多余符号
    word_wipe: list[str]  # 一些需要擦除的字符
    word_replace: dict[str, list[str]]  # 一些需要替换的字符
    cols_names: list[str]  # 创建列索引列名
    cols_show_names: list[str]  # 创建列索引列名（用来看的）
    word_region_start: str  # 起始内容行搜索依据
    word_region_end: list[str]  # 结束内容行搜索依据
    word_offset_start: int  # 行头的实际偏移
    word_offset_end: int  # 行尾的实际偏移
    word_report: list[str]  # 需要报告的错误字符，3% 可能会是396 等
    word_replace_in_col: dict[WordColReplaceNames, str]  # 对不同的列进行不同的过滤，时间列、数据列等


DEFAULT_SETTINGS = {
    "word_report": ["%", "?", "~"],  # 一些必须要肉眼校对的数据，会通过打印数据具体位置
    "word_strip": '. y、",/',  # 一些可能会出现在数据前后的多余符号 -符号需要保留
    "word_wipe": [  # 一些需要擦除的字符
        "'",
        "·",
        "-",
        "一",
        " ",
        "•",
        "■",
        "\\",
        "/",
        "《",
        "’",
        # "，",
        "^",
    ],
    "word_replace": {  # 一些可能会识别错误的字符
        "0": ["()", "o", "p", "U", "u", "〇"],
        "1": ["l", "]", "j", "】", "[", "i"],
        ":": ["：", "；", ";"],
        "8": ["B", "S", "$"],
        ".": ["，", ","],
    },
    "word_replace_in_col": {""},
    "cols_names": list(cps_utils.get_az("A", "T")),  # 创建列索引列名，年检一般是A-T的20列5组数据
    "cols_show_names": ["月", "日", "时分", "水位 (m)", "流量 (m3/s)"] * 4,
    "word_region_start": "曰",  # 起始内容行搜索依据
    "word_region_end": ["—", "-"],  # 结束内容行搜索依据
    "word_offset_start": 2,  # 行头的实际偏移
    "word_offset_end": -2,  # 行尾的实际偏移
}
