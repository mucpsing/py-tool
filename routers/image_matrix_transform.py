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
from fastapi import APIRouter, FastAPI, Form, File
from fastapi import UploadFile, HTTPException, Depends
from loguru import logger

from typing import Optional, NewType
from tools.uploader import Uploader
from config import get_settings, Settings
from Types import Res

from core.image.matrix_transform import (
    ImageMatrixTransform,
    MatrixXY,
    PositionMode,
)

description = """

"""

router = APIRouter()

ParamPoint2D = NewType("x,y", str)


def init(app: FastAPI):
    config = get_settings()

    if not config.image_matrix_enable:
        return

    app.include_router(router)

    @router.post(
        "/image_matrix_transform",
        response_model=Res,
        summary="图片2D矩阵变换",
        description=description,
    )
    def image_matrix_transform_router(
        left_top: ParamPoint2D = Form(None, description="左上角", example="x,y"),
        right_top: ParamPoint2D = Form(None, description="右上角", example="x,y"),
        right_down: ParamPoint2D = Form(None, description="左下角", example="x,y"),
        left_down: ParamPoint2D = Form(None, description="右下角", example="x,y"),
        position_mode: PositionMode = Form(PositionMode.ABSOLUTE),
        file: UploadFile = File(),
        config: Settings = Depends(get_settings),
    ):

        output_path = path.join(config.image_matrix_upload_path, file.filename)

        upload_res = Uploader.stream_file_sync(file, output_path)

        if not upload_res:
            logger.debug(f"{file.filename} 上传失败")
            raise HTTPException(200, detail="上传失败")

        logger.debug(f"文件上传成功{file.filename}")

        # ImageMatrixTransform(upload_res).to_file()
        return Res(msg="入参: ", res=xy.dict())


if __name__ == "__main__":
    pass
