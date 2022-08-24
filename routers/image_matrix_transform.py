# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2022-08-24 09:47:53.357509
# @Last Modified by: CPS
# @Last Modified time: 2022-08-24 09:43:37.592153
# @file_path "W:\CPS\MyProject\python-tools\py-tool\routers"
# @Filename "image_matrix_transform.py"
# @Description: 功能描述
#
if __name__ == "__main__":
    import sys

    sys.path.append("..")
    sys.path.append("../../")

import os
from os import path
from fastapi import APIRouter, FastAPI
from fastapi import UploadFile, HTTPException, Depends
from loguru import logger

from tools.uploader import Uploader
from config import get_settings, Settings
from Types import Res

from core.image.matrix_transform import ImageMatrixTransform

description = """
"""

router = APIRouter()


def init(app: FastAPI):
    config = get_settings()

    if not config.image_matrix_enable:
        return


if __name__ == "__main__":
    pass
