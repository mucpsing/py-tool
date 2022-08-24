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

from core.year_book.split import formater

router = APIRouter()

description = """
## 导出格式为：
| 行            | 内容                                              |
| ------------- | -------------------------------------------------|
| 第一行（列名） | 月   日   时分  流量 (m3/s)   月   日   时分    |
| 第二行（站名） | xxxxx站                                           |
| 第三行（内容） | 真实的数据内容
"""


def init(app: FastAPI):
    config = get_settings()

    if not config.year_book_enable:
        return

    app.include_router(router)

    @router.post(
        "/abby_yearbook_excel_formater",
        response_model=Res,
        summary="年鉴-[洪水水文摘录表]，根据站名按sheet分类重新生成excel文件",
        description=description,
    )
    def year_book_formater_router(
        file: UploadFile, config: Settings = Depends(get_settings)
    ):
        log = logger.add(config.year_book_log_file)

        output_path = path.join(config.year_book_upload_path, file.filename)

        upload_res = Uploader.stream_file_sync(file, output_path)

        logger.info(f"开始处理文件{file.filename}")

        # 通过读取二进制文件头来识别文件格式

        # 上传成功后
        if upload_res:
            format_res = formater(output_path)

            if format_res:
                logger.info(f"{file.filename} => {upload_res}")
                url = f"{config.app_inner_ip}:{config.app_port}{config.year_book_upload_url}/{path.basename(format_res)}"
                return Res(msg="文件处理完成，复制以下url到浏览器下载: ", res={"url": url})

        else:

            logger.warning(f"{file.filename} 上传失败")
            raise HTTPException(200, detail="上传失败")

    return app
