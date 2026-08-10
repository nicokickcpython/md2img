# md2img 工具介绍

md2img 是一条命令把 **Markdown** 转成精美图片的小工具，支持多种模板与尺寸。

> 中文字体使用文泉驿正黑（WenQuanYi Zen Hei），确保中文渲染正常，不会出现乱码或截断。

## 功能特性

- 四种模板：日报 / 卡片 / 海报 / 简洁
- 四种尺寸：长图 / 1:1 / 3:4 / 9:16
- 命令行调用，支持脚本集成与 cron 定时生成

### 表格示例

| 模板 | 尺寸 | 适合场景 |
| ---- | ---- | -------- |
| daily | long | 资讯日报 |
| card | 1:1 | 社交分享 |
| poster | 3:4 | 活动海报 |
| minimal | 9:16 | 手机长图 |

## 代码示例

```python
import md2img
info = md2img.convert_text("# 你好，世界", template="daily", size="long", output="out.png")
print(info)
```

## 引用与列表

1. 第一项：安装依赖
2. 第二项：运行命令
3. 第三项：验证输出

这是一段用于撑高页面、验证多页分页与拼接逻辑的占位文字。它同时包含中文、英文 mixed content 与数字 12345，用于检查换行与自动分页。
