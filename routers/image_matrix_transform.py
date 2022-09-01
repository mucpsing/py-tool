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

from os import path
from fastapi import APIRouter, FastAPI, Form, File
from fastapi import UploadFile, HTTPException, Depends
from fastapi.responses import HTMLResponse
from loguru import logger

from typing import NewType
from tools.uploader import Uploader
from config import get_settings, Settings
from Types import Res

from core.image.matrix_transform import (
    ImageMatrixTransform,
    MatrixXY,
    PositionMode,
)


description = """
## 接口作用
对一张平面的图片进行四角坐标的矩阵变换，以下图片尺寸为
## 参数说明
- "left_top"、"right_top"、"right_down"、"left_down"、对应四角坐标的字符串，用","分割
- 
"""

router = APIRouter(tags=["图片修改"])

ParamPoint2D = NewType("str: 'x,y' 用逗号分割", str)


def init(app: FastAPI):
    config = get_settings()

    if not config.image_matrix_enable:
        return

    app.include_router(router)

    router_path = "image_matrix_transform"
    description = ""
    description_path = path.join(config.app_routers_decs_path, f"{router_path}.md")
    with open(description_path, mode="r", encoding="utf8") as f:
        description = f.read()

    @router.post(
        f"/{router_path}",
        response_model=Res,
        summary="图片2D矩阵变换",
        description="对平面坐标进行矩阵放射变换",
    )
    async def image_matrix_transform_router(
        left_top: ParamPoint2D = Form(
            None, description="左上角坐标", example="`50,50`", title="1,2"
        ),
        right_top: ParamPoint2D = Form(None, description="右上角坐标", example="x,y"),
        right_down: ParamPoint2D = Form(None, description="左下角坐标", example="x,y"),
        left_down: ParamPoint2D = Form(None, description="右下角坐标例", example="x,y"),
        position_mode: PositionMode = Form(
            PositionMode.ABSOLUTE, description="绝对坐标|相对坐标"
        ),
        file: UploadFile = File(),
        config: Settings = Depends(get_settings),
    ):
        sp = ","
        try:
            xy = MatrixXY(
                **{
                    "left_top": tuple(left_top.split(sp)) if left_top else None,
                    "right_top": tuple(right_top.split(sp)) if right_top else None,
                    "right_down": tuple(right_down.split(sp)) if right_down else None,
                    "left_down": tuple(left_down.split(sp)) if left_down else None,
                }
            )
        except Exception as e:
            raise HTTPException(200, detail=f"上传失败{e}")

        output_path = path.join(config.image_matrix_upload_path, file.filename)
        upload_res = await Uploader.stream_file_sync(file, output_path)

        if not upload_res:
            logger.debug(f"{file.filename} 上传失败")
            raise HTTPException(200, detail="上传失败")

        logger.debug(f"文件上传成功{file.filename}")
        to_file_res = ImageMatrixTransform(output_path, xy, position_mode).to_file()
        if to_file_res:
            url = f"{config.image_matrix_upload_url}/{path.basename(to_file_res)}"
            return Res(msg="入参: ", res={"url": url})

    @router.get(
        f"/{router_path}", tags=["test"], summary="带vewer的接口", description=description
    )
    def render():
        return HTMLResponse(
            """
    <form id="form">
        左上角坐标: <input type="text" name="left_top" value="" placeholder="50,50">
        <br>

        右上角坐标: <input type="text" name="left_top" value="" placeholder="x,y">
        <br>

        左下角坐标: <input type="text" name="right_down" value="" placeholder="50,50">
        <br>

        右下角坐标: <input type="text" name="left_down" value="" placeholder="x,y">
        <br>

        <label for="position_mode">坐标模式:</label>
        <select name="position_mode" id="position_mode">
            <option value="absolute">绝对定位</option>
            <option value="relative">相对定位</option>
        </select><br>

        <input type="file" name="file">
    </form>

    <button onclick="upload()">提交</button>

    <script>
        function upload() {
            var formElement = document.getElementById("form");

            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/upload_file");
            xhr.send(new FormData(formElement));
        }
    </script>"""
        )


if __name__ == "__main__":
    pass
