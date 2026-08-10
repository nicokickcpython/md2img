# Markdown 语法全景测试文档

> 用途：作为 `md2img` 渲染器的回归测试样本，**覆盖全部主流 Markdown 语法**。本文以中文叙述为主、穿插英文术语与代码片段，意在贴近真实写作场景，并自然撑满 2 至 3 页 A4，方便验证分页、换行、表格断行与图片位置等排版细节。

---

## 一、标题层级 H1 — H4

# 一级标题：项目背景与目标

## 二级标题：功能范围与边界

### 三级标题：核心模块拆解

#### 四级标题：解析器实现要点

> 备注：HTML 端若启用 `h5/h6`，可继续追加 `#####` 与 `######`，本测试聚焦 H1–H4 已足够覆盖大部分文档结构。

---

## 二、段落、换行与强调

这是一段普通正文，演示中文长段落排版：第一句说明语义，第二句插入一个 *斜体强调*，第三句使用 **加粗强调**，第四句混合 ***加粗 + 斜体***，第五句给出 ~~删除线~~ 与 ==高亮== 标记（高亮依赖扩展语法）。段落末尾的连续两个空格  
表示强制换行（line break），下一行紧跟其后。

第二段继续说明：行内可同时出现 `inline code`、**bold** 与 *italic*，再夹一段 [外部链接](https://example.com "悬停提示文本") 用于检验锚文本与悬停样式。

- 上标示例：E = mc^2^
- 下标示例：H~2~O
- 缩写：Markdown 规范由 [CommonMark] 定义，部分扩展来自 GFM (GitHub Flavored Markdown)。

[CommonMark]: https://commonmark.org/

---

## 三、列表：有序、无序、嵌套与任务列表

### 3.1 无序列表（实心圆点）

- 顶层项 A
  - 嵌套项 A-1
    - 嵌套项 A-1-a
    - 嵌套项 A-1-b（含 **加粗** 与 `code`）
  - 嵌套项 A-2
- 顶层项 B
  - [x] 已完成任务（任务列表）
  - [ ] 未完成任务
  - [ ] ~~取消的任务~~（演示删除线在复选框中的应用）

### 3.2 有序列表（编号自动续号）

1. 第一步：准备输入文件
2. 第二步：调用解析器
   1. 子步骤 2.1：词法分析
   2. 子步骤 2.2：语法树构建
3. 第三步：渲染输出
4. 第四步：校验排版

### 3.3 定义列表（扩展语法）

术语 A
: 术语 A 的解释，用于解释 Markdown 相关概念。

术语 B
: 术语 B 的解释，强调与术语 A 的区别。

---

## 四、代码块：行内与围栏

行内示例：调用 `render(markdown)` 函数即可生成图片，参数 `theme="dark"` 启用深色主题。

围栏代码块（指定语言）：

```typescript
// TypeScript 示例：计算斐波那契数列
export function fib(n: number): number {
  if (n < 2) return n;
  let [a, b] = [0, 1];
  for (let i = 2; i <= n; i++) {
    [a, b] = [b, a + b];
  }
  return b;
}

const result = fib(10);
console.log(`fib(10) = ${result}`);
```

```python
# Python 示例：读取 Markdown 并统计字数
from pathlib import Path

text = Path("README.md").read_text(encoding="utf-8")
print(f"chars={len(text)}, lines={text.count(chr(10))+1}")
```

```bash
# Shell 示例：批量转换
for f in docs/*.md; do
  md2img "$f" -o "${f%.md}.png"
done
```

无语言标记的代码块（用于展示原始排版）：

```
纯文本块    多余空格
  缩进应被保留
```

---

## 五、表格与对齐

| 语法     |     含义 | 示例                | 渲染说明              |
| :------- | -------: | :-----------------: | :-------------------- |
| 标题     |   章节名 | `# 一级`            | 字号最大、加粗        |
| 列表     |   条目   | `- item`            | 缩进层级清晰          |
| 表格     |   矩阵   | `\| a \| b \|`      | 支持左/右/居中对齐    |
| 代码     |     块   | ` ```ts `           | 保留缩进与高亮        |
| 图片     |     图   | `![alt](url)`       | 支持本地与远程        |
| emoji    |   表情   | `:tada:` / 🎉       | 短码与 Unicode 双通道 |

| 左对齐列1 | 左对齐列2 | 左对齐列3 |
| :-------- | :-------- | :-------- |
| 数据 A1   | 数据 A2   | 数据 A3   |
| 数据 B1   | 数据 B2   | 数据 B3   |

| 居中对齐列 | 内容 |
| :--------: | :--: |
| 文本 1     |  √   |
| 文本 2     |  ×   |

| 数值（千分位） | 科学计数 | 百分比 |
| -------------:| --------:| ------:|
|        1,234.5 |  1.2e+3  | 78.6%  |
|      999,000.0 |  9.99e+5 | 99.9%  |

---

## 六、引用与嵌套

> 一级引用：Markdown 起源于 2004 年的 `Markdown.pl`，目标是让"易读易写"的纯文本成为可发布结构。
>
> > 二级嵌套引用：CommonMark 规范明确了 12 类核心元素的解析规则，是当前最权威的参考实现。
> >
> > > 三级嵌套引用：GFM 在此基础上扩展了表格、任务列表与删除线，被 GitHub、GitLab 等平台广泛采用。
>
> 回到一级：在引用块中同样支持 **加粗**、*斜体*、`inline code` 与 [链接](https://spec.commonmark.org/)。

---

## 七、链接、图片与自动链接

- 普通链接：[md2img 项目主页](https://github.com/example/md2img)
- 悬停提示：[带 title 的链接](https://commonmark.org/ "CommonMark 规范")
- 相对路径：[本地文档](README.md)
- 锚点链接：[回到章节](#一、标题层级-h1--h4)
- 自动链接：<https://www.markdownguide.org/>
- 邮箱自动链接：<[email protected]>

图片示例（远程占位）：

![md2img 渲染示意](https://placehold.co/600x240/2563eb/ffffff?text=md2img+render "渲染示意图")

带尺寸的图片（HTML 扩展，部分渲染器支持）：

<img src="https://placehold.co/320x120/16a34a/ffffff?text=logo" alt="logo" width="320" height="120" />

---

## 八、分割线

第一段内容，下面是一条 `---` 分割线。

---

第二段内容，下面是 `***` 分割线。

***

第三段内容，下面是 `___` 分割线。

___

---

## 九、脚注

Markdown 在 GFM 规范下支持脚注语法[^1]，常用于补充引用与延伸阅读[^bible]。脚注可出现多次引用[^1]，并允许自定义标签。

长段落中嵌入脚注：CommonMark 本身未定义脚注[^cm]，但 Pandoc、GFM、Typora 等实现提供了扩展支持[^pandoc]，使得学术写作也能享受纯文本的便利。

[^1]: 这是第一个脚注，用于演示基本语法。
[^bible]: 脚注标签可自定义，例如 `bible`、`ref-2026` 等。
[^cm]: 参见 https://spec.commonmark.org/
[^pandoc]: 参见 Pandoc 手册：https://pandoc.org/MANUAL.html

---

## 十、Emoji 与符号

短码写法：`:tada:` `:rocket:` `:fire:` `:white_check_mark:` `:x:` `:bulb:` `:warning:` `:lock:` `:key:` `:sparkles:`

Unicode 直写：🎉 🚀 🔥 ✅ ❌ 💡 ⚠️ 🔒 🔑 ✨ 🐛 📦 🛠️ 🧪 🇨🇳 🇺🇸

数学与单位符号：∑ ∏ √ ∞ ≠ ≈ π Ω ° ′ ″ ¥ € $ £

箭头与几何：← → ↑ ↓ ↔ ⇒ ⇔ △ ○ ☆ ★ ♡ ♥ ♦ ♣

---

## 十一、中英混排、长 URL、特殊字符与 HTML 实体

中英混排是真实写作的常态：The `md2img` tool supports `inline code`、*italic* 与 **bold**，并能正确处理 *smart quotes*——例如 "中文双引号" 与 "English double quotes" 的差异，以及 '中文单引号' 与 'English single quotes' 的细节。

长 URL 测试（需正确换行或保持完整）：

- 普通长链接：https://example.com/very/long/path/to/resource?query=markdown&lang=zh-CN&v=2026.08.10&token=abcdef0123456789
- 带端口与锚点：https://docs.example.com:8443/guide/getting-started/installation.html#section-3-2-configure
- 多个查询参数：https://api.example.com/v2/search?q=md2img&page=1&size=20&sort=desc&filter[status]=active&filter[type]=image

HTML 实体与特殊字符：

- 小于号：&lt; 渲染为 `<`
- 大于号：&gt; 渲染为 `>`
- 与号：&amp; 渲染为 `&`
- 版权符：&copy; 渲染为 `©`
- 注册商标：&reg; 渲染为 `®`
- 商标：&trade; 渲染为 `™`
- 不间断空格：`a&nbsp;b` 中间为不间断空格
- 中文标点：，。、；：？！「」『』（）【】《》
- 全角破折号：—— 与连接号 –
- 省略号：……

转义字符：`\*`、`\_`、`\\`、`\[`、`\]`、`` \` ``、`\{`、`\}` 都不应触发对应语法。

---

## 十二、数学公式

行内公式：质能方程 $E = mc^2$ 是爱因斯坦的著名结论，欧拉恒等式 $e^{i\pi} + 1 = 0$ 被誉为最美公式。

块级公式（KaTeX / MathJax 风格）：

$$
\int_{-\infty}^{+\infty} e^{-x^2}\, dx = \sqrt{\pi}
$$

矩阵示例：

$$
A = \begin{pmatrix}
a_{11} & a_{12} & a_{13} \\
a_{21} & a_{22} & a_{23} \\
a_{31} & a_{32} & a_{33}
\end{pmatrix}
$$

分段函数：

$$
f(x) = \begin{cases}
x^2, & x \ge 0 \\
-x,  & x < 0
\end{cases}
$$

求和与极限：

$$
\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}, \qquad
\lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n = e
$$

---

## 十三、HTML 块与原始片段

Markdown 允许在文档中直接嵌入 HTML，用于补充 Markdown 难以表达的细节：

<details>
<summary>点击展开：md2img 的设计目标</summary>

1. 忠实还原 GitHub / Typora 渲染效果；
2. 支持自定义主题与字体；
3. 支持长文自动分页（A4 / Letter）；
4. 输出 PNG / WebP / SVG。

</details>

键盘按键：使用 `<kbd>` 标签表示 <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>P</kbd> 打开命令面板。

---

## 十四、综合长段落（用于压测排版）

在真实写作中，作者常常在一段之内混合：中文叙述、英文术语、行内代码、加粗强调、斜体强调、删除线、高亮、脚注引用、外部链接、自动链接、Emoji、HTML 实体与数学公式。例如：我们在 `render(src, { theme: "dark", pageSize: "A4" })`[^1] 中传入参数，`theme="dark"` 启用深色主题；当主题切换至 `"light"` 时，背景由 `#0f172a` 变为 `#ffffff`，主色由 `#60a5fa` 变为 `#2563eb`，对比度始终满足 WCAG AA 标准。再如：方程 $a^2 + b^2 = c^2$ 是勾股定理，毕达哥拉斯学派称其为 *"百牛之祭"*；此外，需注意 smart quotes 的处理——`"hello"` 与 `"hello"`、`'world'` 与 `'world'` 在不同语言环境下应被正确区分。最终输出会被传入 `compress(quality=0.92)` 进行有损压缩，体积通常能下降 60%~80%，却几乎察觉不到画质损失 👍。

---

## 十五、语法覆盖清单

| #  | 语法类别         | 具体覆盖项                                                                                                   |
| -- | :--------------- | :----------------------------------------------------------------------------------------------------------- |
| 1  | 标题             | H1–H4（`#`–`####`）                                                                                          |
| 2  | 段落与换行       | 普通段落、强制换行（双空格 + 回车）、空行分段                                                                 |
| 3  | 行内强调         | `**粗体**`、`*斜体*`、`***粗斜体***`、`~~删除线~~`、`==高亮==`                                                |
| 4  | 行内代码         | `` `inline code` ``                                                                                          |
| 5  | 代码块           | ``` ```ts ```、``` ```python ```、``` ```bash ```、无语言代码块                                                |
| 6  | 无序列表         | `-`、`*`、`+`，三层嵌套                                                                                      |
| 7  | 有序列表         | `1.` 起始，自动续号，子编号缩进                                                                              |
| 8  | 任务列表         | `- [x]` / `- [ ]`、含删除线                                                                                  |
| 9  | 表格             | 列对齐（左/右/居中）、多行、含千分位与百分号                                                                 |
| 10 | 引用             | `>`、三级嵌套，含行内格式                                                                                    |
| 11 | 链接             | 普通、悬停 title、相对路径、锚点、自动链接 `<url>`、邮箱                                                      |
| 12 | 图片             | `![alt](url "title")`、HTML `<img>` 带尺寸                                                                   |
| 13 | 分割线           | `---`、`***`、`___`                                                                                          |
| 14 | 脚注             | `[^id]` 引用、`[^id]: 定义`，自定义标签，多次引用                                                             |
| 15 | Emoji            | 短码 `:tada:`、Unicode 🎉🚀🔥、旗帜、数学符号、箭头几何                                                       |
| 16 | 中英混排         | 中英文标点对照、smart quotes 双引号/单引号                                                                     |
| 17 | 长 URL           | 多段超长查询参数、带端口与锚点                                                                                |
| 18 | 特殊字符         | `*` `_` `[]` `` ` `` `{}` 等转义                                                                              |
| 19 | HTML 实体        | `&lt;` `&gt;` `&amp;` `&copy;` `&reg;` `&trade;` `&nbsp;`                                                    |
| 20 | 数学公式         | 行内 `$..$`、块级 `$$..$$`、矩阵、分段函数、极限、求和、积分                                                  |
| 21 | HTML 块          | `<details>`、`<summary>`、`<kbd>`、`<img width/height>`                                                       |
| 22 | 扩展语法         | 上下标 `^` `~`、缩写 `[abbr]:`、`mark` 高亮                                                                   |

> **统计**：本清单共覆盖 **22** 大类语法（涵盖约 **40** 项具体子语法），文档路径为 `/opt/data/code/md2img/scripts/md-syntax-test.md`。
