# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2022-09-05 10:37:00.724465
# @Last Modified by: CPS
# @Last Modified time: 2022-09-05 10:37:00.724465
# @file_path "W:\CPS\MyProject\python-tools\py-tool\utils"
# @Filename "dir_to_zip.py"
# @Description: 功能描述
#
if __name__ == "__main__":
    import sys

    sys.path.append("..")
    sys.path.append("../../")

import zipfile, os


def dir_to_zip(
    file_dir: str, *, output_name: str = None, file_list: list[str] = None
) -> str:
    """
    传入一个目录，将该目录压缩成zip文件

    - param file_dir       :{str}       要压缩的目录
    - param output_name    :{str}       压缩后导出的位置（绝对路径）
    - param file_list=None :{list[str]} 指定哪些文件需要压缩，默认该目录下所有文件

    @returns `{str}` 如果成功返回压缩包名字，如果失败返回空""字符串
    @example
    ```python
    tar_dir = r'xxxx/'
    res = dir_to_zip(tar_dir)

    if not res: return print('压缩失败')
    ```
    """

    res = ""
    if not output_name:
        name = os.path.basename(file_dir).split(".")[0]
        output_name = os.path.join(file_dir, f"{name}.zip")

    if not file_list:
        file_list = os.listdir(file_dir)

    cur_dir = os.getcwd()
    try:
        os.chdir(file_dir)
        with zipfile.ZipFile(output_name, "w") as z:
            for each in file_list:

                z.write(each, compress_type=zipfile.ZIP_DEFLATED)
        res = output_name
    except Exception as e:
        print("z.write fail: ", e)

    finally:
        os.chdir(cur_dir)
        return res
