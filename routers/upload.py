# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2022-05-28 12:09:02.355571
# @Last Modified by: CPS
# @Last Modified time: 2022-05-28 12:09:02.355571
# @file_path "D:\CPS\MyProject\demo\cps-cli\cps-cli-template-fastapi\routers"
# @Filename "upload.py"
# @Description: 试调页面：host:port/file/test
#
import sys
from os import path

sys.path.append("..")
from fastapi import APIRouter, FastAPI, File, Form
from fastapi import UploadFile, Depends, HTTPException, HTMLResponse

from config import get_settings, Settings
from Types import Res, Err, Fileinfo

router = APIRouter()


def init(app: FastAPI):
    app.include_router(router)

    @router.post("/upload_file")
    async def upload_file(
        firstName: str,
        lastName: str,
        file: UploadFile,
        config: Settings = Depends(get_settings),
    ):
        output_path = path.join(config.upload_path, file.filename)

        upload_res = await Uploader.stream_file(file, output_path)

        if upload_res:
            return Res(
                msg="上传成功",
                res={
                    "content_type": file.content_type,
                    "file_name": file.filename,
                    "output_path": output_path,
                },
            )
        else:
            raise HTTPException(detail="上传失败")

    @router.get("/upload_file_view")
    async def viewer():
        return HTMLResponse(
            """
<form id="form">
    左上角坐标: <input type="text" name="left_top" value="Mickey">
    <br>

    右上角坐标: <input type="text" name="left_top" value="Mouse">
    <br>

    左下角坐标: <input type="text" name="right_down" value="Mouse">
    <br>

    右下角坐标: <input type="text" name="left_down" value="Mouse">
    <br>

    坐标模式:
    <label for="position_mode">坐标模式:</label>
    <select name="pets" id="position_mode">
        <option value="">--Please choose an option--</option>
        <option value="dog">Dog</option>
        <option value="cat">Cat</option>
        <option value="hamster">Hamster</option>
        <option value="parrot">Parrot</option>
        <option value="spider">Spider</option>
        <option value="goldfish">Goldfish</option>
    </select>

    <input type="file" name="file"><br>
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

    return app
