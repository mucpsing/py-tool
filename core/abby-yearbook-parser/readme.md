# 项目结构
```yaml
【Root】
   |-- split.py    # 将name_xxxx.xlsx的文件按照站名分割成不同的sheet
   |-- readme.md   #
   |-- main.py     # 过滤abby导出的文件成 name_xxxx.xlsx => 然后手动检查错误

```

# usage
`main.py`（基础的过滤数据） => `手动检查` => `plit.py`（最终数据按sheet输出）
