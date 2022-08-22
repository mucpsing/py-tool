from utils import index as cps_utils

STATION_NAMES = [
    "小古箓站",
    "飞来峡站",
    "石角站",
    "坪石（二）站",
    "犁市（二）站",
    "滃江站",
    "高道站",
    "珠坑站",
]


DEFAULT_SETTINGS = {
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
