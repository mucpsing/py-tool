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

router = APIRouter(tags=["年鉴识别"])

description = """
# 处理ABBY识别后导出的xlsx结果文件
（仅限年鉴的洪水水文摘录表）

## 使用步骤
- 上传abby识别后的excel文件
- 下载过滤后的文件，进行肉眼检查。。。
- 调用另一个接口上传文件进行格式化

## 注意事项:
- 数据需要手动确保为20列，有时候abby会识别成21列，首要手动修复
"""


def init(app: FastAPI):
    config = get_settings()

    if not config.year_book_enable:
        return

    config.year_book_settings = ABBYYearBookExcelFilter.CreateSettings(DEFAULT_SETTINGS)
    app.include_router(router)

    @router.post(
        "/abby_yearbook_excel_parser",
        response_model=Res,
        summary="年鉴-[洪水水文摘录表]，处理通过abby识别后导出的excel文件（确保20列数据）",
        description=description,
    )
    def year_book_filter(file: UploadFile, config: Settings = Depends(get_settings)):
        log = logger.add(config.year_book_log_file)

        output_path = path.join(config.year_book_upload_path, file.filename)

        upload_res = Uploader.stream_file_sync(file, output_path)

        logger.debug(f"开始处理文件{file.filename}")

        # 通过读取二进制文件头来识别文件格式

        # 上传成功后
        if upload_res:
            abby_parser = ABBYYearBookExcelFilter(
                output_path, config.year_book_settings
            )

            output_excel = abby_parser.to_file(split_sheet=True)

            url = f"{config.app_inner_ip}:{config.app_port}{config.year_book_upload_url}/{path.basename(output_excel)}"

            logger.debug(f"{file.filename} => {upload_res}")

            return Res(msg="文件处理完成，复制以下url到浏览器下载: ", res={"url": url})

        else:

            logger.debug(f"{file.filename} 上传失败")
            raise HTTPException(200, detail="上传失败")

    return app
