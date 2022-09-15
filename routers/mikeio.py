# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2022-08-22 18:55:24.424667
# @Last Modified by: CPS
# @Last Modified time: 2022-08-22 18:55:24.424667
# @file_path "D:\CPS\MyProject\Projects_Personal\py-tool\routers"
# @Filename "year_book.py"
# @Description: 功能描述
#
import os, sys

sys.path.append("..")

from os import path
from fastapi import APIRouter, FastAPI
from fastapi import UploadFile, HTTPException, Depends
from loguru import logger


from tools.uploader import Uploader
from config import get_settings, Settings
from Types import Res

from core.mikepy.to_shp import mike_file_to_shp

# from core.mikepy.to_xyz import dfsu_to_xyz

router = APIRouter(tags=["mike21-FM"], prefix="/mikeio")


def init(app: FastAPI):
    config = get_settings()

    if not config.mikeio_enable:
        return

    description = ""
    router_name = "mikeio"
    description_path = path.join(config.app_routers_decs_path, f"{router_name}.md")
    with open(description_path, mode="r", encoding="utf8") as f:
        description = f.read()

    app.include_router(router)

    @router.post(
        "/to_shp",
        response_model=Res,
        summary="导出dfsu文件的数据为xyz格式",
        description=description,
    )
    def to_shp(file: UploadFile, config: Settings = Depends(get_settings)):
        log = logger.add(config.mikeio_log_file)

        filename, ext = path.splitext(file.filename)

        upload_file = path.join(config.mikeio_upload_path, file.filename)
        upload_res = Uploader.stream_file(file, upload_file)
        output_dir = f"{path.join(config.mikeio_output_path, filename)}"

        logger.debug(f"开始处理文件{file.filename} =>=> {output_dir}")

        # 上传成功后
        if upload_res:
            output = mike_file_to_shp(upload_file, output_dir)
            if not output:
                Res(msg=f"文件处理失败{file.filename}", success=False)

            url = f"{config.app_inner_ip}:{config.app_port}{config.mikeio_upload_url}/{filename}"
            return Res(msg="文件处理完成，复制以下url到浏览器下载: ", res={"url": url})

        else:

            logger.debug(f"{file.filename} 上传失败")
            raise HTTPException(200, detail="上传失败")

    return app
