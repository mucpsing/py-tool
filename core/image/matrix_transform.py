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
from typing import NewType

PIL_IMG = NewType("Image.open()", object)
Coords2D = NewType("[x:int, y:int]", list[int])
XY_OBJ = NewType("{'left_top':(x:int, y:int), .../}", dict[str, tuple[int, int]])
XY_LIST = NewType("[(x:int, y:int), .../]", list[tuple[int, int]])


class PositionMode(enum.Enum):
    ABSOLUTE = 0  # 声明当前坐标是绝对坐标
    RELATIVE = 1  # 声明当前坐标是相对坐标


class ImageMatrixTransform:
    relative_xy_template = {
        "left_top": [0, 0],
        "right_top": [0, 0],
        "right_down": [0, 0],
        "left_down": [0, 0],
    }

    def __init__(
        self, img: str, xy: XY_OBJ = None, mode: PositionMode = PositionMode.ABSOLUTE
    ):
        self.img_path = img
        self.img = Image.open(img).convert("RGBA")
        self.mode = mode  # absolute | relative 相对坐标或者绝对坐标
        self.transform_img = None  # 用来存放改变透视后的图片实例
        self.xy_obj = {
            "left_top": [0, 0],
            "right_top": [self.img.width, 0],
            "right_down": [self.img.width, self.img.height],
            "left_down": [0, self.img.height],
        }

        # ["left_top", "right_top", "right_down", "left_down"]
        self.xy_list: XY_LIST = list()

        if xy:
            self.transform(xy)

    @property
    def result(self) -> PIL_IMG:
        return self.transform_img

    def to_file(self, output_path: str = "") -> str:
        if not output_path:
            dirname = path.dirname(self.img_path)
            name, ext = path.splitext(path.basename(self.img_path))
            output_path = path.join(
                dirname, f"{name}_{int(time.time())}_transform{ext}"
            )

        if self.transform_img:
            self.transform_img.save(output_path)

        return output_path

    def to_show(self):
        if self.transform_img:
            self.transform_img.show()
        return self

    def transform(self, xy: XY_OBJ = None):
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

    def conver_xy_obj_2_list(self, xy_obj: XY_OBJ) -> XY_LIST:
        """
        将四点坐标转换为数组，然后使用np能更快的计算，入参采用对象的方式，入参不用每个位置都输入坐标，更自由

        - param xy_obj :{Coordinates2D} 对象形式的坐标点信息，类型仅作提示，不需实际采用

        @example
        ```py
        # input
        {
            "left_top": (0, 0),
            "right_top": (1, 1),
            "right_down": (2, 2),
            "left_down": (3, 3),
        }

        # output
        [(0,0), (1, 1), (2, 2), (3, 3)]
        ```
        """

        if self.mode == PositionMode.ABSOLUTE:
            self.xy_obj.update(xy_obj)
            return [
                self.xy_obj["left_top"],
                self.xy_obj["right_top"],
                self.xy_obj["right_down"],
                self.xy_obj["left_down"],
            ]

        elif self.mode == PositionMode.RELATIVE:
            # 使用更新对象的方式，入参不用每个位置都输入坐标，更自由
            nxy = ImageMatrixTransform.relative_xy_template
            nxy.update(xy_obj)
            return [
                nxy["left_top"],
                (self.img.width + nxy["right_top"][0], nxy["right_top"][1]),
                (
                    self.img.width + nxy["right_down"][0],
                    self.img.height + nxy["right_down"][1],
                ),
                (nxy["left_down"][0], self.img.height + nxy["left_down"][1]),
            ]

        # 返回测试坐标
        return [(50, 50), (250, 250), (300, 300), (50, 350)]

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
    tar: str = r"./test/test.png"
    xy = {"left_top": (50, 150)}

    tar = ImageMatrixTransform(tar, xy=xy).to_show().to_file()
