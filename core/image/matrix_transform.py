# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date:
# @Last Modified by: CPS
# @Last Modified time: 2022-08-24 09:43:37.592153
# @file_path "W:\CPS\MyProject\python-tools\py-tool\core\image"
# @Filename "matrix_transform.py"
# @Description: 图片的2D矩阵变换，支持使用绝对坐标或者相对坐标，手动指定mode
#

import enum, time
from PIL import Image
from os import path
from typing import NewType, Optional, TypeAlias

from pydantic import BaseModel

PIL_IMG = NewType("Image.open()", object)
Point2D: TypeAlias = tuple[int, int]
XY_LIST: TypeAlias = list[Point2D]


class MatrixXY(BaseModel):
    left_top: Optional[Point2D] = None
    right_top: Optional[Point2D] = None
    right_down: Optional[Point2D] = None
    left_down: Optional[Point2D] = None


class PositionMode(str, enum.Enum):
    ABSOLUTE = "absolute"  # 声明当前坐标是绝对坐标
    RELATIVE = "relative"  # 声明当前坐标是相对坐标


class ImageMatrixTransform:
    relative_xy_template = {
        "left_top": [0, 0],
        "right_top": [0, 0],
        "right_down": [0, 0],
        "left_down": [0, 0],
    }

    def __init__(
        self, img: str, xy: MatrixXY = None, mode: PositionMode = PositionMode.ABSOLUTE
    ):
        self.img_path = img
        self.img = Image.open(img).convert("RGBA")
        self.mode = mode  # absolute | relative 相对坐标或者绝对坐标
        self.transform_img: PIL_IMG = None  # 用来存放改变透视后的图片实例
        self.img_xy_obj = MatrixXY(
            **{
                "left_top": [0, 0],
                "right_top": [self.img.width, 0],
                "right_down": [self.img.width, self.img.height],
                "left_down": [0, self.img.height],
            }
        )

        # ["left_top", "right_top", "right_down", "left_down"]
        self.xy_list: XY_LIST = list()

        if xy:
            self.transform(xy)

    def __del__(self):
        self.img.close()
        self.transform_img.close()

    @property
    def result(self) -> PIL_IMG:
        return self.transform_img

    def to_file(self, output_path: str = "") -> str:
        try:
            if not output_path:
                dirname = path.dirname(self.img_path)
                name, ext = path.splitext(path.basename(self.img_path))
                output_path = path.join(
                    dirname, f"{name}_{int(time.time())}_transform{ext}"
                )

            if self.transform_img:
                self.transform_img.save(output_path)

            return output_path
        except Exception as e:
            print("to_file fail", e)
            return ""

    def to_show(self):
        if self.transform_img:
            self.transform_img.show()
        return self

    def transform(self, xy: MatrixXY = None):
        if xy:
            self.xy_list = self.conver_xy_obj_2_list(xy)

        # 配置背景矩阵范围
        bg_range = [
            (0, 0),
            (self.img.width, 0),
            (self.img.width, self.img.height),
            (0, self.img.height),
        ]

        # 拼接参数作为仿射计算函数的入参
        transform = self.PerspectiveTransform(bg_range, self.xy_list)

        self.transform_img = self.img.transform(
            size=self.img.size,
            method=Image.Transform.PERSPECTIVE,
            data=transform,
            resample=Image.Resampling.NEAREST,
        )

        return self

    def conver_xy_obj_2_list(self, new_xy_obj: MatrixXY) -> XY_LIST:
        """
        将四点坐标转换为数组，然后使用np能更快的计算，入参采用对象的方式，入参不用每个位置都输入坐标，更自由

        - param new_xy_obj :{MatrixXY} 对象形式的坐标点信息，类型仅作提示，不需实际采用

        @example
        ```py
        # output
        XY_LIST[(0,0), (1, 1), (2, 2), (3, 3)]
        ```
        """

        if self.mode == PositionMode.ABSOLUTE:
            base_xy = self.img_xy_obj.dict()
            base_xy.update(new_xy_obj.dict(exclude_none=True))

            return (
                base_xy["left_top"],
                base_xy["right_top"],
                base_xy["right_down"],
                base_xy["left_down"],
            )

        elif self.mode == PositionMode.RELATIVE:
            base_xy = {**ImageMatrixTransform.relative_xy_template}
            base_xy.update(new_xy_obj.dict(exclude_none=True))

            return (
                base_xy["left_top"],
                (self.img.width + base_xy["right_top"][0], base_xy["right_top"][1]),
                (
                    self.img.width + base_xy["right_down"][0],
                    self.img.height + base_xy["right_down"][1],
                ),
                (base_xy["left_down"][0], self.img.height + base_xy["left_down"][1]),
            )

        # 返回测试坐标
        return ((50, 50), (250, 250), (300, 300), (50, 350))

    @staticmethod
    def PerspectiveTransform(background_xy: XY_LIST, front_xy: XY_LIST) -> XY_LIST:
        """
        坐标点顺序： [left_top, right_top, right_down, left_down]

        - param background_xy :{list} 背景原尺寸的四角坐标，`[(0, 0), (img_width, 0), (img_width, img_height), (0, img_height)]`
        - param front_xy      :{list} 需要仿射的新坐标，`[[95, 134], [95, 134], [195, 209], [195, 209]]`

        @returns `{ list}` 二维数据，每一维带8个元素

        """
        import numpy as np

        matrix = []
        for p1, p2 in zip(front_xy, background_xy):
            matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
            matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])
        A = np.matrix(matrix, dtype=np.float64)
        B = np.array(background_xy).reshape(8)
        res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
        return np.array(res).reshape(8)


if __name__ == "__main__":
    tar: str = r"../../test/test.png"

    xy = MatrixXY(left_top=(50, 150), right_down=None)
    print("xy: ", xy.dict(exclude_unset=True))

    # tar = ImageMatrixTransform(tar, xy=xy).to_show().to_file()
