import os
from os import path

from pydantic import BaseSettings
from functools import lru_cache

import Types as T
from docs.description import DESCRIPTION, LICENSE_INFO, CONTACT
from core.year_book.abby import ABBYYearBookExcelFilterSettings
from utils.index import get_inside_ip

ROOT_PATH = os.getcwd()
STATIC_PATH = path.join(ROOT_PATH, "static")


class Settings(BaseSettings):
    DEV: bool = True  # 是否开发模式

    app_name: str = "CPS 自用FastApi脚手架"
    app_host: str = "0.0.0.0"  # 地址
    app_port: int = 4040  # 端口
    app_version: str = "v1"
    app_description: str = DESCRIPTION
    app_routers_decs_path: str = path.join(ROOT_PATH, "docs")
    app_contact: dict = CONTACT
    app_license_info: dict = LICENSE_INFO
    app_inner_ip: str = get_inside_ip()

    # 日志相关
    log_enable: bool = True
    log_level: str = "debug"  # 日志等级
    log_engine: str = "loguru"  # 日志引擎
    log_path: str = path.join(ROOT_PATH, "logs")  # 日志目录

    # 常用功能开关
    enable_schedule: bool = False  # 是否开启定时任务
    enable_gzip: bool = False  # 是否开启gzip亚索
    enable_cors: bool = False  # 是否开启跨域
    enable_upload: bool = True  # 是否开启上传文件接口

    # api 文档配置
    swagger_enable: bool = True
    swagger_route: str = "/docs"
    redoc_enable: bool = True
    redoc_route: str = "/redoc"

    # Redis 配置
    redis_enable: bool = False
    redis_options: T.RedisOptions = None

    # 静态目录配置
    static_enable: bool = True  # 开启静态服务
    static_path: str = path.join(ROOT_PATH, "static")
    static_route: str = "/static"

    # 上传配置
    upload_enable: bool = True
    upload_path: str = path.join(ROOT_PATH, "static", "upload")

    # 年鉴接口配置
    year_book_enable: bool = True
    year_book_upload_url: str = "/static/year_book/result"
    year_book_upload_path: str = path.join(ROOT_PATH, "static/year_book/result")
    year_book_settings: ABBYYearBookExcelFilterSettings = None
    year_book_log_file: str = path.join(ROOT_PATH, "logs", "year_book.log")

    # 图片相关接口配置
    image_matrix_enable: bool = True
    image_matrix_upload_url: str = "/static/upload/image/matrix_transform"
    image_matrix_upload_path: str = path.join(
        STATIC_PATH, "upload/image/matrix_transform"
    )

    # mike接口相关
    mikeio_enable: bool = True
    mikeio_upload_path: str = path.join(ROOT_PATH, "static/upload/mikeio")
    mikeio_output_path: str = path.join(ROOT_PATH, "static/upload/mikeio/shp")
    mikeio_upload_url: str = "/static/upload/mikeio/shp"
    mikeio_log_file: str = path.join(ROOT_PATH, "logs", "mikeio.log")

    class Config:
        env_file: str = path.join(ROOT_PATH, "config.ini")  # 读取失败


# settings = Settings()
# 缓存配置文件到cache，不用每次调用接口都读取文件io
@lru_cache
def get_settings():
    print("run get_settings()")
    return Settings()
