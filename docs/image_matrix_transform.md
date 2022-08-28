# 接口入参

这是一个支持参数的Form文件上传接口，<a href="/test/image_matrix_transform">实际地址</a>

HTML代码参考

```
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
</script>
```



| 参数名称        | 类型       | 示例                         | 说明                           |
| --------------- | ---------- | ---------------------------- | ------------------------------ |
| `left_top`      | str        | `"50,150"`                   | 左上角坐标，中间用`","`分割    |
| `right_top`     | str        | `"50,150"`                   | 右上角坐标，中间用`","`分割    |
| `right_down`    | str        | `"50,150"`                   | 右下角坐标，中间用`","`分割    |
| `left_down`     | str        | `"50,150"`                   | 左下角坐标，中间用`","`分割    |
| `position_mode` | str        | `"absolute"`|`"relative"`    | 是以绝对定位还是相对定位来修改 |
| **file**        | 二进制形式 | 前端通过Form标签或者示例添加 | 二进制形式的File，             |



## 测试地址：

- <a href="/image_matrix_transform_test">测试接口</a>
- [swagger](http://localhost:4040/docs#/default/image_matrix_transform_router_image_matrix_transform_post)

