# -*- coding: utf-8 -*-
#
# @Author: CPS
# @email: 373704015@qq.com
# @Date: 2022-08-17 10:38:24.441329
# @Last Modified by: CPS
# @Last Modified time: 2022-08-17 10:38:24.441329
# @file_path "W:\CPS\MyProject\test"
# @Filename "excel_test.py"
# @Description: 用来处理ABBY识别后导出的xlsx结果文件
#


if __name__ == "__main__":
    import sys

    sys.path.append("..")
    sys.path.append("../../")


import os, time
from os import path
from typing import Optional


import pandas as pd
from pandas import DataFrame, Series
from loguru import logger as lg
from pydantic import BaseModel

from utils import index as cps_utils

# import cps_utils


class ABBYYearBookExcelFilterSettings(BaseModel):
    fix_24_to_new_day: bool = True  # 部分年鉴会使用24作为小时单位，修复后改位置变成0，日数据添加1
    fix_24_col_names: list[str] = ["C", "H", "M", "R"]
    word_strip: str  # 一些在数据前后的多余符号
    word_wipe: list[str]  # 一些需要擦除的字符
    word_replace: dict[str, list[str]]  # 一些需要替换的字符
    cols_names: list[str]  # 创建列索引列名
    cols_show_names: list[str]  # 创建列索引列名（用来看的）
    word_region_start: str  # 起始内容行搜索依据
    word_region_end: list[str]  # 结束内容行搜索依据
    word_offset_start: int  # 行头的实际偏移
    word_offset_end: int  # 行尾的实际偏移
    word_report: list[str]  # 需要报告的错误字符，3% 可能会是396 等


class ContextRegion(BaseModel):
    row_start: int
    row_end: int


class RegionInfo(BaseModel):
    region: ContextRegion  # 数据范围
    count: int  # 序号
    title_row_index: int = -1  # 是否存在标题行
    page: int = -1  # 当前内容的页码
    station_name: Optional[str]  # 站名


class ABBYYearBookExcelFilter:
    @staticmethod
    def CreateSettings(options):
        return ABBYYearBookExcelFilterSettings(**options)

    def __init__(self, target: str, settings: ABBYYearBookExcelFilterSettings):
        self.table = pd.DataFrame([])
        self.source = target
        self.settings = settings
        self.data_region_list: list[RegionInfo] = list()

        # 状态记录
        self.pre_col_name: str = ""  # 上一列的列名
        self.next_col_name: str = ""  # 下一列的列名
        self.currt_col_name: str = ""  # 当前列名
        self.currt_row_index: int = -1  # 当前处理数据的具体位置（currt_col_name）

        # 读取数据到self.table中
        self.__open_excel(target)

        # 输入数据的基本检查
        self.__check_data()

        # 每一列遍历，根据规律，识别出数据的大体位置
        self.__get_data_region()

        # 分析内容，将同一个水文站的内容合并
        self.__merge_region()

        # 首页过滤
        self.__first_page_filter()

        # 预览数据
        self.__show_data()

        # 过滤数据
        # 遍历每列，调用self.col_handler来处理每列的数据
        for each_col_name in self.settings.cols_names:
            self.currt_col_name = each_col_name
            self.col_handler(self.table[each_col_name])
            self.pre_col_name = each_col_name

    # 读取excel文件
    def __open_excel(self, excel_file_path: str):
        self.table: DataFrame = pd.read_excel(
            excel_file_path,
            names=self.settings.cols_names,  # 列名
            dtype="str",  # 指定所有数据为字符串
            index_col=False,  # 第一列不指定任何索引（默认从0开始）
            header=None,  # 表头
        )
        return self

    def __check_data(self) -> bool:
        """
        数据格式检查函数
        """

        # 1、列数检查
        # 检查列数是否于settings里面指定的列名数量相同，如果不相同，可能需要手动优化
        row_len = len(self.settings.cols_names)
        row_len_data = self.table.shape[1]

        if row_len != row_len_data:
            lg.exception(f"当前列数{row_len}于数据真实列数不匹配 {row_len_data}")
            return False

        # 2、时间列检查，时分的列数据为25

        return True

    def __show_data(self):
        [print(cps_utils.print_dict(each.dict())) for each in self.data_region_list]
        print("处理结果")
        print("行数,列数: ", self.table.shape)
        print("当前处理的总页数: ", self.data_region_list[-1].count)
        return self

    @lg.catch
    def check_row_has_page_num(self, row_data: list, find_list: list[str]) -> bool:
        """
        对数据行进行监测，判断是否页码行

        - param row_data  :{list}      列数据
        - param find_list :{list[str]} 用来判断是否页码行的收个元素条件：["—", "-"]

        @returns `{ bool }`

        """
        # setp1: 根据find_list的条件判断
        first_cell = str(row_data[0]).strip()
        for find_str in find_list:
            if first_cell.find(find_str) == 0:
                return True

        # setp2: 当前行只有第一个元素有值
        rest_cell_len = 0
        for each in row_data[1:]:
            # 检查元素是否为空
            if isinstance(each, str):
                rest_cell_len += len(each)

        # 除了第一个元素，还有其他有内容的元素，证明不是页面行
        if rest_cell_len > 0:
            return False

        # 尝试获取页面
        is_page = cps_utils.get_int(row_data[0])
        if is_page > -1:
            return True

        pd.ExcelFile

        return False

    def find_station_name(self, row_data_list: Series) -> str:
        """
        通过遍历行，查找站名

        - param row_data_list :{Series} {description}

        @returns `{ str}` {description}

        """

        # 条件1： 第一列数据基本是没有内容的
        if isinstance(row_data_list[0], str):
            return ""

        found = ""
        word_list = []
        for each_value in row_data_list[1:]:
            if not isinstance(each_value, str):
                continue

            if cps_utils.is_contains_chinese(each_value.strip()):
                found = True
                word_list.append(str(each_value))

        if found:
            return "".join(word_list)

        return ""

    @lg.catch
    def __get_data_region(self):
        """
        获取数据有效范围，将所有范围保存成列表：`self.data_region_list`

        ```py
        [{
            region: tuple[int, int]             # 数据范围
            count: int                          # 序号
            title_row_index: Optional[int] = None   # 是否存在标题行
            page: Optional[int] = None          # 当前内容的页码
        }, ...{}]
        ```
        """
        start = self.settings.word_region_start  # 起始内容行搜索依据
        end = self.settings.word_region_end  # 结束内容行搜索依据
        start_offset = self.settings.word_offset_start  # 行头的实际偏移
        end_offset = self.settings.word_offset_end  # 行尾的实际偏移

        row_start = -1  # 数据真实范围-起始行
        row_end = -1  # 结束行
        count = 1  # 当前是第几个内容区，对应实际识别的页数

        title_row_index: int = -1  # 标题所在的行
        station_name: str = None  # 站名
        in_contaion = False  # 状态：表示当前是否再实际内容范围中

        row_index = 0
        for row in self.table.itertuples(index=False):
            row_index += 1

            # 查找站名
            if not isinstance(row[0], str) and in_contaion:
                # 查找中文标题
                has_station_name = self.find_station_name(row)
                if has_station_name:
                    title_row_index = row_index
                    station_name = has_station_name

                continue

            # 查找数据真实位置
            tar = str(row[0]).strip()
            if tar.find(start) == 0:
                in_contaion = True
                row_start = row_index + start_offset

            elif self.check_row_has_page_num(row, end) and in_contaion:
                # 获取页码
                page = cps_utils.get_int(tar)
                row_end = row_index + end_offset

                self.data_region_list.append(
                    RegionInfo(
                        region=ContextRegion(row_start=row_start, row_end=row_end),
                        count=count,
                        title_row_index=title_row_index,
                        page=page,
                        station_name=station_name,
                    )
                )

                title_row_index = -1
                in_contaion = False
                row_start = -1
                row_end = -1
                count += 1

        return self

    @lg.catch
    def __merge_region(self) -> list[RegionInfo]:
        """
        过滤当前的数据列表，处理标题行在数据列表中的各种情况
        """
        pre_page = -1
        new_region: list[RegionInfo] = list()
        for index in range(len(self.data_region_list)):
            region_info = self.data_region_list[index]
            pre_last_region: RegionInfo = None

            # 存在标题行
            if region_info.title_row_index > -1:
                # 当站名行在最前时，忽略站名行
                if region_info.region.row_start == region_info.title_row_index:
                    region_info.region.row_start = region_info.region.row_start + 1

                # 站名行在中间
                elif (
                    region_info.region.row_start
                    < region_info.title_row_index
                    < region_info.region.row_end
                ):
                    # 连续页的处理情况
                    if region_info.page - pre_page == 1:
                        # 添加一个新的实例来分割新旧页面的内容
                        # 属于前一个站的数据
                        pre_region = self.data_region_list[index - 1]
                        region_copy = self.data_region_list[index].dict()
                        region_copy.update(
                            {
                                "station_name": pre_region.station_name,
                                "region": ContextRegion(
                                    row_start=region_info.region.row_start,
                                    row_end=region_info.title_row_index - 1,
                                ),
                            }
                        )
                        pre_last_region = RegionInfo(**region_copy)

                    # 标题
                    region_info.region.row_start = region_info.title_row_index + 1

                    # 修复
                    region_info.region.row_end = region_info.region.row_end - 1

            pre_page = region_info.page

            # 如果有新的数据，先添加新数据
            if pre_last_region:
                new_region.append(pre_last_region)
            new_region.append(region_info)

        if len(new_region) > len(self.data_region_list):
            self.data_region_list = new_region

        return self

    def __first_page_filter(self):
        # 当第一页存在标题行，且标题行不在最前面
        # 去掉标题行之前的内容
        first_region = self.data_region_list[0]

        if first_region.title_row_index > first_region.region.row_start:
            self.data_region_list[0].region.row_start = first_region.title_row_index + 1

        return self

    def col_handler(self, col_data: Series):
        """
        对传入的列数据进行遍历

        - param col_data :{Series} 列数据

        """
        pre_page = None
        for each_region_info in self.data_region_list:
            region = each_region_info.region
            # -1 修复一个BUG，实际数据范围需要-1
            for index in range(region.row_start - 1, region.row_end):
                self.currt_row_index = index
                tar = col_data[index]

                # 不是字符串不进行处理
                if not isinstance(tar, str):
                    continue

                # 数据过滤
                new_data = self.__cell_filter(tar)

                # 修复时列数据为25的问题
                # if (
                #     self.settings.fix_24_to_new_day
                #     and self.currt_col_name in self.settings.fix_24_col_names
                # ):
                #     new_data = self.fix_24_on_time_cols(new_data)

                # 最终写入数据
                col_data[index] = new_data

    def fix_24_on_time_cols(self, cell_content: str) -> str:
        """
        修复小时列为25的数据
        """
        if cell_content == "24":
            # 获取日期列的数据
            pre_col_data = self.table[self.pre_col_name]
            search_index = self.currt_row_index

            for i in range(70):
                cell_data = pre_col_data[search_index]
                if isinstance(cell_data, str) and len(cell_data.strip()) > 0:

                    self.table[self.pre_col_name][self.currt_row_index] = str(
                        int(cell_data) + 1
                    )
                    return "0"
                    break
                search_index -= 1

            print(f"发现24小时时间单位问题: [{self.currt_col_name}{self.currt_row_index + 1 }]")
            return cell_content

        return cell_content

    def __cell_filter(self, cell_content: str) -> str:
        # word_wipe 过滤
        for each in self.settings.word_wipe:
            cell_content = cell_content.replace(each, "")

        # word_strip 过滤
        cell_content = cell_content.strip(self.settings.word_strip)

        # 空格过滤
        cell_content = cell_content.replace(" ", "")

        # word_replace 过滤
        # 替换数据，根据self.settings.word_replace字典来遍历
        for replace_words, search_words in self.settings.word_replace.items():
            for index in range(len(search_words)):
                for search_word in search_words[index]:
                    if search_word in cell_content:
                        cell_content = cell_content.replace(search_word, replace_words)
        return cell_content

    def to_file(self, output_name: str = None, split_sheet: bool = False) -> str:
        """
        导出数据为excel，

        - param output_name       :{str}  {description}
        - param split_sheet=False :{bool} 是否到出以站名作为sheet名分类好的excel

        """
        dir_name = path.dirname(self.source)
        name, ext = path.splitext(path.basename(self.source))

        if not output_name:
            output_name = path.join(dir_name, f"{name}_{int(time.time())}{ext}")

        if not split_sheet:
            self.table.to_excel(output_name, index=False, header=False)
            return self

        # 按sheet导出，根据标题
        data = {}
        for index in range(len(self.data_region_list)):
            region_info = self.data_region_list[index]
            if not region_info.station_name in data:
                # 添加站名行和一个空行做分隔
                data[region_info.station_name] = [
                    pd.DataFrame(
                        [
                            {"A": " "},
                            {
                                "A": "start",
                                "B": region_info.station_name,
                                "C": region_info.page,
                            },
                        ]
                    ),
                ]

            data[region_info.station_name].append(
                self.table[
                    region_info.region.row_start - 1 : region_info.region.row_end
                ]
            )
            # data[region_info.station_name].append(region_info.region)

        print(data.keys())
        output_excel = pd.ExcelWriter(output_name)

        new_data = []
        # self.table.to_excel(output_excel, index=False, header=False)
        for sheet_name, data_region_list in data.items():
            # 合并所有数据
            sheet_data = pd.concat(data_region_list)
            new_data.append(sheet_data)

        new_data = pd.concat(new_data)
        new_data.to_excel(
            output_excel, header=self.settings.cols_show_names, index=False
        )
        output_excel.save()
        return output_name

    def __len__(self):
        return len(self.data_region_list)

    def __del__(self):
        self.table = None


def test(tar: str):
    table = pd.read_excel(tar, dtype="str", index_col=False)

    l = 0
    for row in table.itertuples():
        print(row[0])

        l += 1
        if l > 100:
            break


if __name__ == "__main__":
    # 必须手动处理的情况
    # 1、 Abby识别后，数据的列数不是等于20列，需要手动处理所有数据为20列（A~T）

    # BUG
    # 1、 内容结束区紧靠一个 - 来识别准确，需要将后面是否有其他列内容加入判断中（>9）
    # 2、 可能存在单个空格的空数据列

    # 配置
    settings = ABBYYearBookExcelFilter.CreateSettings(
        {
            "word_report": ["%", "?", "~"],  # 一些必须要肉眼校对的数据，会通过打印数据具体位置
            "word_strip": '. y、",/',  # 一些可能会出现在数据前后的多余符号 -符号需要保留
            "word_wipe": [  # 一些需要擦除的字符
                "'",
                "·",
                "-",
                "一",
                " ",
                "•",
                "■",
                "\\",
                "/",
                "《",
                "’",
                "，",
                "^",
            ],
            "word_replace": {  # 一些可能会识别错误的字符
                "0": ["()", "o", "p", "U", "u", "〇"],
                "1": ["l", "]", "j", "】", "[", "i"],
                ":": ["：", "；", ";"],
                "8": ["B", "S", "$"],
            },
            "cols_names": list(cps_utils.get_az("A", "T")),  # 创建列索引列名，年检一般是A-T的20列5组数据
            "cols_show_names": ["月", "日", "时分", "水位 (m)", "流量 (m3/s)"] * 4,
            "word_region_start": "曰",  # 起始内容行搜索依据
            "word_region_end": ["—", "-"],  # 结束内容行搜索依据
            "word_offset_start": 2,  # 行头的实际偏移
            "word_offset_end": -2,  # 行尾的实际偏移
        }
    )
    # show settings
    # cps_utils.print_dict(settings.dict())

    # usage
    target = path.realpath(r"./data/2012.xlsx")
    res = ABBYYearBookExcelFilter(target, settings)
    res.to_file(split_sheet=True)

    # test(target)
