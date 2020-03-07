# doubanSpider
豆瓣TOP250基于css选择器和xpath的提取



# 1. CSS选择器

在 CSS 中，选择器是一种模式，用于选择需要添加样式的元素。

"CSS" 列指示该属性是在哪个 CSS 版本中定义的。（CSS1、CSS2 还是 CSS3。）

w3c指南：<https://www.w3school.com.cn/cssref/css_selectors.ASP>

| 选择器                 | 例子            | 例子描述                                 |
| :--------------------- | :-------------- | :--------------------------------------- |
| .*class*               | .intro          | 选择 class="intro" 的所有元素。          |
| #id                    | #firstname      | 选择 id="firstname" 的所有元素。         |
| *                      | *               | 选择所有元素。                           |
| element                | p               | 选择所有 <p> 元素。                      |
| *element*,*element*    | div,p           | 选择所有 <div> 元素和所有 <p> 元素。     |
| *element* *element*    | div p           | 选择 <div> 元素内部的所有 <p> 元素。     |
| *element*>*element*    | div>p           | 选择父元素为 <div> 元素的所有 <p> 元素。 |
| [*attribute*\]         | [target]        | 选择带有 target 属性所有元素。           |
| [*attribute*=*value*\] | [target=_blank] | 选择 target="_blank" 的所有元素。        |

## 1.1 标签选择器

标签选择器其实就是我们经常说的html代码中的标签。例如html、span、p、div、a、img等等；比如我们想要设置网页中的p标签内一段文字的字体和颜色，那么css代码就如下所示：

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>标签选择器</title>
</head>
<style>
    p{
        color: #f00;
        font-size: 16px;
    }
</style>
<body>
<p>css标签选择器的介绍</p>
<p>标签选择器、类选择器、ID选择器</p>
<a href="https://www.baidu.com">百度一下</a>
</body>
</html>
```

## 1.2 类选择器

类选择器在我们今后的css样式编码中是最常用到的，它是通过为元素设置单独的class来赋予元素样式效果。

**使用语法：**（我们这里为p标签单独设置一个类选择器.content,代码就如下所示）

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>类选择器</title>
</head>
<style>
    .content{
        color: #f00;
        font-size: 16px;
    }
</style>
<body>
<p>css标签选择器的介绍</p>
<p class="content">标签选择器、类选择器、ID选择器</p>
</body>
</html>
```

**详细讲解：**

1、类选择器都是使用英文圆点（.）开头；

2、每个元素可以有多个类名，，名称可以任意起名（但不要起中文，一般都是与内容相关的英文缩写）

3、类选择器只会改变类下的元素样式，而不会改变其它标签的默认样式；

我们上边的页面在浏览器上显示的效果就如下所示：（content下的文字内容颜色变成了红色，字体变成了16px）

## 1.3 ID选择器

ID选择器类似于类选择符，作用同类选择符相同，但也有一些重要的区别。

**使用语法：**

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ID择器</title>
</head>
<style>
    #content{
        color: #f00;
        font-size: 16px;
    }
</style>
<body>
<p>css标签选择器的介绍</p>
<p id="content">标签选择器、类选择器、ID选择器</p>
</body>
</html>
```

**详细讲解：**

1、ID选择器为标签设置id="ID名称"，而不是class="类名称"。

2、ID选择符的前面是符号为井号（#），而不是英文圆点（.）。

3、ID选择器的名称是唯一的，即相同名称的id选择器在一个页面只能出现一次；

## 1.4 组合选择器

可以多个选择器一起使用，就是组合选择器

## 1.5 伪类选择器

可以用 :: 指定选择标签的属性。

| :last-child        | p:last-child        | 选择所有p元素的最后一个子元素          |
| ------------------ | ------------------- | -------------------------------------- |
| :last-of-type      | p:last-of-type      | 选择每个p元素是其母元素的最后一个p元素 |
| :not(selector)     | :not(p)             | 选择所有p以外的元素                    |
| :nth-child(n)      | p:nth-child(2)      | 选择所有 p 元素的父元素的第二个子元素  |
| :nth-last-child(n) | p:nth-last-child(2) | 选择所有p元素倒数的第二个子元素        |

## 1.6 属性提取器

```python
import requests
import parsel

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}

response = requests.get('https://maoyan.com/board/4?offset=0', headers=headers)
html = response.text

# %% 标签选择器
sel = parsel.Selector(html)
# 提取 p 标签
ps = sel.css('p')
for p in ps:
    print(p.get())

# %% 类（class）选择器
ps = sel.css('.star')
for p in ps:
    print(p.get())

# %% id选择器
ps = sel.css('#app')
for p in ps:
    print(p.get())

# %% 组合选择器
# ps = sel.css('#app .star')
ps = sel.css('div#app .star')
for p in ps:
    print(p.get())

# %% 伪类选择器
# ps = sel.css('#app .star')
ps = sel.css('div#app .star::text')
for p in ps:
    print(p.get())

# %% 属性选择器
names = sel.css('p.name a::attr(title)').extract()
print(names)

# %% 案例:猫眼电影

```

# 4. XPath数据提取

## 4.1XPath介绍

XPath (XML Path Language) 是一门在 XML 文档中查找信息的语言，可用来在 XML/HTML 文档中对元素和属性进行遍历，并提取相应元素。

也是一种数据提取方式，只不过针对的是HTML/XML数据，因为爬虫主要和HTML页面打交道。

### 4.2 XPath匹配规则

下表是XPath常用的规则：

![](../../../%E9%9D%92%E7%81%AF%E6%95%99%E8%82%B2%E7%88%AC%E8%99%AB%E7%AC%AC%E4%B8%89%E6%9C%9F/03-%E6%95%B0%E6%8D%AE%E8%A7%A3%E6%9E%90/assets/1561599466458.png)

