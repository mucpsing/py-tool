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

from core.year_book.abby import ABBYYearBookExcelFilter
from core.year_book.config import DEFAULT_SETTINGS

router = APIRouter()


def init(app: FastAPI):
    config = get_settings()

    if not config.year_book_enable:
        return

    app.include_router(router)
    config.year_book_settings = ABBYYearBookExcelFilter.CreateSettings(DEFAULT_SETTINGS)

    @router.post("/year_book", response_model=Res, summary="上传psd、字体、图片等文件")
    async def year_book_router(
        file: UploadFile, config: Settings = Depends(get_settings)
    ):
        log = logger.add(config.year_book_log_file)

        output_path = path(config.year_book_upload_path, file.filename)

        upload_res = await Uploader.stream_file(file, output_path)

        logger.info(f"开始处理文件{file.filename}")

        # 通过读取二进制文件头来识别文件格式

        # 上传成功后
        if upload_res:
            abby_parser = ABBYYearBookExcelFilter(
                output_path, config.year_book_settings
            )

            output_excel = abby_parser.to_file(split_sheet=True)

            url = f"{config.year_book_upload_path}/{output_excel}"

            logger.info(f"{file.filename} => {upload_res}")

            return Res(msg="文件处理完成，复制以下url到浏览器下载: ", res={"url": url})

        else:

            logger.warning(f"{file.filename} 上传失败")
            raise HTTPException(detail="上传失败")

    return app
