# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2022-09-08 14:40:02.761606
# @Last Modified by: CPS
# @Last Modified time: 2022-09-08 14:40:02.761606
# @file_path "W:\CPS\MyProject\python-tools\py-tool\core\year_book"
# @Filename "cps_utils.py"
# @Description: 工具类，存放一些工具函数
#
if __name__ == "__main__":
    import sys

    sys.path.append("..")
    sys.path.append("../../")

import os, time
from os import path

from pydantic import BaseModel
from functools import wraps


def get_az(start: str | int, end: str | int = None) -> str:
    """
    获取英文字母

    - param start :{str|int} 起始英文字母，如果输入数字，默认从A开始
    - param end   :{str|int} 结束的英文字母

    @returns `{str}` {description}
    @example
    ```py
    # 获取A之后10个英文字母
    res = get_az("A", 10)
    >>> ABCDEFGHIJ

    # 获取a到f的字母
    res = get_az("a", 'f')
    >>> abcde
    ```
    """
    import string

    AZ = string.ascii_uppercase
    az = string.ascii_lowercase
    ret = f"{AZ}{az}"

    # 数字
    if isinstance(start, int):
        if isinstance(end, int) and end > start:
            return ret[start:end]

        return ret[start:]

    # 传入字符串
    elif isinstance(start, str):
        start_num = ret.find(start[0])
        if isinstance(end, str):
            end_num = ret.find(end[0])
            # 需要+1来修正确实到指定的end字符
            return ret[start_num : end_num + 1]
        elif isinstance(end, int):
            return ret[start_num:end]
        return ret[start_num:]


def is_contains_chinese(tar: str) -> bool:
    """检验是否含有中文字符"""
    for _char in tar:
        if "\u4e00" <= _char <= "\u9fff":
            return True
    return False


def get_int(tar: str) -> int:
    try:
        return int("".join(list(filter(str.isdigit, tar))))
    except:
        return -1


def print_dict(target: dict, indent: int = 4) -> str:
    import json

    print("dict_json: ", json.dumps(target, indent=indent, ensure_ascii=False))


# 创建一个装饰器函数
def func_timeit(count=1):
    """
    计算一个函数式的执行时间

    - param count=1 :{int} 重复多少次

    @example
    ```python
    @func_timeit(100)
    def test(): pass
    ```
    """

    def detector(func):
        @wraps(func)
        def run(*args, **key):
            # 需要在func前运行的代码
            start = time.time()

            res = None
            for i in range(count):
                res = func(*args, **key)

            end = time.time()
            print(f"{func.__name__}[{count}] => {round(end-start, 3)}(ms)")

            return res

        return run

    return detector


def get_output_name(intput_name: str) -> str:
    """
    返回一个与源文件名字相似，添加了时间后缀的文件名

    @example
    ```python
    input = r"./ccvb.xlsx"
    print(get_output_name(t))

    >>> ".\ccvb_1662619457.xlsx"
    ```
    """
    dir_name = path.dirname(intput_name)
    name, ext = path.splitext(path.basename(intput_name))
    output_name = path.join(dir_name, f"{name}_{int(time.time())}{ext}")
    return output_name


if __name__ == "__main__":
    target = " --__-  －－-１  sss２ asdfasdf ０ 。  "
    t = "./ccvb.xlsx"

    print(get_output_name(t))
