# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date:
# @Last Modified by: CPS
# @Last Modified time: 2022-05-26 20:55:54.506017
# @file_path "D:\CPS\MyProject\外接项目\PSD文件解析\psd-tools"
# @Filename "app.py"
# @Description: 功能描述
#

import uvicorn
from fastapi import FastAPI, Depends


from config import get_settings, Settings

from utils import logger
from events import startup
from routers import docs, static
from routers import year_book_parser, year_book_formart, image_matrix_transform
from routers import mikeio

config = get_settings()
app = FastAPI(
    title=config.app_name,
    description=config.app_description,
    version=config.app_version,
    contact=config.app_contact,
    docs_url=None,
    redoc_url=None,
)

startup.init(app)
# upload.init(app)1111

logger.init(app)
static.init(app)
docs.init(app)


year_book_parser.init(app)
year_book_formart.init(app)
image_matrix_transform.init(app)
mikeio.init(app)

if config.DEV:
    from routers import test

    app.include_router(test.router)

# @app.get("/", summary="显示当前服务器所有配置 （开发模式下）")
# async def root(settings: Settings = Depends(get_settings)):
#     return {"msg": "当前服务器配置", **settings.dict()}

# @app.get("/exit", summary="退出服务器 （开发模式下）")
# async def Exit():
#     exit()

# @app.get("/restart", summary="重启服务器 （开发模式下）")
# async def restart():
#     exit()


if __name__ == "__main__":
    from os import path

    file_name = path.splitext(path.basename(__file__))[0]

    # 使用这种方式有点问题，热加载失效
    # Config = uvicorn.Config(
    #     f"{file_name}:app",
    #     host=config.app_host,  # 地址
    #     port=config.app_port,  # 端口
    #     log_level=config.log_level,  # 日志等级
    #     reload=config.DEV,  # 热更新
    #     reload_excludes=[".git"],
    # )
    # Server = uvicorn.Server(Config)
    # Server.run()

    uvicorn.run(
        f"{file_name}:app",
        host=config.app_host,  # 地址
        port=config.app_port,  # 端口
        log_level=config.log_level,  # 日志等级
        reload=config.DEV,  # 热更新
        reload_excludes=[".git"],
    )
