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
import enum, time
import sys

sys.path.append("..")

from os import path
from fastapi import APIRouter, FastAPI, Form
from fastapi import UploadFile, HTTPException, Depends, File
from loguru import logger

from tools.uploader import Uploader
from config import get_settings, Settings
from Types import Res

from core.mikepy.to_shp import mike_file_to_shp
from core.mikepy.to_file import dfsu_to_file, DataItem

from utils.compress import dir_to_zip

router_name = "mikeio"
router = APIRouter(tags=["mike21-FM"], prefix=f"/{router_name}")


def init(app: FastAPI):
    config = get_settings()

    if not config.mikeio_enable:
        return

    # 读取文档
    # description = ""
    # description_path = path.join(config.app_routers_decs_path, f"{router_name}.md")
    # with open(description_path, mode="r", encoding="utf8") as f:
    #     description = f.read()

    app.include_router(router)

    @router.post(
        "/dfsu_to_polygon_shp",
        response_model=Res,
        summary="提取dfsu的边界为shp面文件，并打包成zip",
    )
    def to_polygon_shp(
        file: UploadFile = File(...),
        config: Settings = Depends(get_settings),
        output_name: str = Form(None, description="结果文件的名称（不用带后缀）"),
        over_write: bool = Form(True, description="已存在文件是否覆盖"),
    ):
        # log = logger.add(config.mikeio_log_file)

        filename, ext = path.splitext(file.filename)
        upload_file = path.join(config.mikeio_upload_path, file.filename)

        # 判断文件是否已经存在
        if path.exists(upload_file) and not over_write:
            upload_res = upload_file
        else:
            upload_res = Uploader.stream_file(file, upload_file)

        # 指定保存的位置和文件名称
        if output_name:
            outout_zip = path.join(config.mikeio_output_path, f"{output_name}.zip")
            url = f"{config.app_inner_ip}:{config.app_port}{config.mikeio_upload_url}/{path.basename(outout_zip)}"
            output_dir = path.join(config.mikeio_output_path, output_name)

        else:
            outout_zip = None
            url = f"{config.app_inner_ip}:{config.app_port}{config.mikeio_upload_url}/{filename}/{path.basename(file.filename)}"
            output_dir = path.join(config.mikeio_output_path, filename)

        logger.debug(f"开始处理文件{file.filename} =>=> {output_dir}")
        # 上传成功后
        if upload_res:
            output = mike_file_to_shp(upload_file, output_dir)
            if not output:
                Res(msg=f"文件处理失败{file.filename}", success=False)

            zip_res = dir_to_zip(output_dir, exclude=[filename], output_name=outout_zip)
            if not zip_res:
                Res(msg=f"文件压缩失败{file.filename}", success=False)

            return Res(msg="文件处理完成，复制以下url到浏览器下载: ", res={"url": url})

        logger.debug(f"{file.filename} 上传失败")
        raise HTTPException(200, detail="上传失败")

    @router.post(
        "/dfsu_to_file", summary="获取dfsu文件指定时间和项目的数据，导出成xyz的文件", response_model=Res
    )
    def to_file(
        file: UploadFile = File(...),
        config: Settings = Depends(get_settings),
        item: DataItem = Form(
            DataItem.speed,
            description="流速: `Current speed`| 流向: `Current direction`",
        ),
        setp: int = Form(-1, description="要提取的时间步进，0为第一个，-1为最后一个，以此类推"),
        output_name: str = Form(
            None, description="结果文件的名称，当前支持后缀 `xls`|`xlsx`|`xyz`|`txt`|`shp`"
        ),
        over_write: bool = Form(True, description="已存在文件是否覆盖"),
    ):

        filename, ext = path.splitext(file.filename)
        upload_file = path.join(config.mikeio_upload_path, file.filename)

        # 判断文件是否已经存在
        if path.exists(upload_file) and not over_write:
            upload_res = upload_file
        else:
            logger.debug("文件已存在，当前进行覆盖")
            upload_res = Uploader.stream_file(file, upload_file)

        # 配置输出成成
        if output_name:
            output_full_name = path.join(config.mikeio_output_path, output_name)
        else:
            output_full_name = path.join(
                config.mikeio_output_path, f"{filename}_{item}_{int(time.time())}.xyz"
            )

        # 上传成功后
        if upload_res:
            logger.debug(f"output name:  {output_full_name}")
            output = dfsu_to_file(
                upload_file, out_file=output_full_name, item=item, setp=setp
            )
            if not output:
                Res(msg=f"文件处理失败{file.filename}", success=False)
            url = f"{config.app_inner_ip}:{config.app_port}{config.mikeio_upload_url}/{path.basename(output)}"
            return Res(msg="文件处理完成，复制以下url到浏览器下载: ", res={"url": url})

        logger.debug(f"{file.filename} 上传失败")
        raise HTTPException(200, detail="上传失败")

    return app
