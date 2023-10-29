## json简介

JSON是一种轻量级的数据交换格式。 易于人阅读和编写。同时也易于机器解析和生成。 它基于JavaScript Programming Language, Standard ECMA-262 3rd Edition - December 1999的一个子集。 JSON采用完全独立于语言的文本格式，但是也使用了类似于C语言家族的习惯（包括C, C++, C#, Java, JavaScript, Perl, Python等）。 这些特性使JSON成为理想的数据交换语言。

## json在线解析及格式化工具介绍

JSON格式化和JSON验证器工具帮助自动格式化JSON和验证您的JSON文本。它还提供了一个树视图,帮助导航格式化的JSON数据。

![json格式化工具截图](https://upload-images.jianshu.io/upload_images/3360192-2a0a6c09efd022dc.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


体验地址是：https://fktool.com/json/

# 源码分享

```
<!DOCTYPE html>
<html lang="zh-CN">

<head>
    <title>JSON在线解析 | JSON在线格式化校验工具</title>
    <meta charset="utf-8" />
    <meta name="viewport"
        content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=5.0, user-scalable=yes" />
    <meta name="applicable-device" content="pc,mobile" />
    <meta name="keywords" content="json格式化, json在线解析, json校验" />
    <meta name="description"
        content="一个功能强大的在线 JSON 解析和格式化工具,提供JSON在线,json解析,json在线解析,JSON Formatter,json数组,JSON校验,格式化JSON,xml转json工具,在线json格式化工具,json格式化,json格式化工具,json字符串格式化,json在线,json在线验证,json在线校验" />

    <!-- Google -->
    <meta itemprop="name" content="json在线解析工具" />
    <meta itemprop="description" content="一个功能强大的在线 JSON 解析和格式化工具..." />
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="json在线解析工具" />
    <meta name="twitter:description" content="一个功能强大的在线 JSON 解析和格式化工具..." />

    <meta name="renderer" content="webkit" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <link rel="icon" type="image/png" href="/images/favicon_48x48.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/images/favicon_114x114.png">
    <link rel="icon" href="/images/favicon.ico" type="image/x-icon" />
    <link href="https://cdn.staticfile.org/twitter-bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet"
        type="text/css" />
    <link href="./static/style/tool.css" rel="stylesheet" type="text/css" />

</head>

<body>

    <header class="hd-nav">
        <a class="navbar-icon" href="/">
            <img src="/images/icon_36x36.svg" width="32" height="32" alt="fktool在线工具网" />
            <span class="navbar-label">FKTool.com</span>
        </a>
    </header>

    <div class="main">
        <div class="left">
            <div class="row">
                <h1 style="font-size: 24px;margin: 16px 16px;color:#7952b3;">JSON在线格式化工具</h1>
            </div>
            <div class="row">
                <div class="banner">输入要解析的json文本并点击格式化按钮</div>
            </div>
            <div class="row">
                <div class="col-md-12 col10main">
                    <div class="accordion" id="accordion2">
                        <div class="accordion-group">
                            <div class="panel panel-defaul">
                                <form id="form1" class="form-horizontal" method="post">
                                    <div class="input-group mb5"><input class="form-control" type="text" id="txt_url"
                                            placeholder="输入远程Json网址" /><span class="input-group-btn"><button
                                                class="btn btn-default" type="button"
                                                id="get_remote">远程获取Json</button></span></div>
                                    <div class="form-group">
                                        <div class="col-sm-12"><textarea id="content" name="content"
                                                class="form-control" rows="14"
                                                placeholder="请输入Json，Json格式化的时候要去除所有转义，转义存在可能导致Json校验不通过"></textarea>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <div class="col-sm-12 text-center">

                                            <input type="button" class="btn btn-success" name="validate" id="validate"
                                                value="Json格式化" />
                                            <input type="button" class="btn btn-info" onclick="jsonzip(1);"
                                                value="Json压缩">
                                            <span id="copyallcode" class="btn btn-default"
                                                data-clipboard-target="#content">复制</span>
                                            <input type="button" class="btn btn-default" onclick="content.value=''"
                                                value="清空">
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <div class="col-sm-12">
                                            <div class="alert alert-warning alert-dismissible text-left" role="alert"
                                                id="results"><span>请输入需要格式化的Json字符串</span></div>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                        <div class="alert alert-info main-desc">
                            <h2 class="f20">json在线解析及格式化工具介绍</h2>
                            <p>
                                JSON格式化和JSON验证器工具帮助自动格式化JSON和验证您的JSON文本。它还提供了一个树视图,帮助导航格式化的JSON数据。它具有如下优点:
                            </p>

                            <ul>
                                <li>
                                    它有助于通过错误消息在线验证JSON。
                                </li>
                                <li>
                                    它是唯一的JSON工具，显示图像悬停在树视图中的图像URL。
                                </li>
                                <li>
                                    它也是一个JSON美化器，支持缩进级别:2个空格，3个空格和4个空格。
                                </li>
                                <li>
                                    支持打印JSON数据。
                                </li>
                                <li>
                                    JSON文件格式化器提供了上传JSON文件和下载格式化JSON文件的功能。这个功能有助于格式化json文件。
                                </li>
                                <li>
                                    95%的API使用JSON在客户端和服务器之间传输数据。这个工具可以作为API格式化器使用。
                                </li>
                                <li>
                                    支持JSON字符串的JSON图形视图，作为JSON调试器或纠错器，可以格式化数组和对象。
                                </li>
                                <li>
                                    在浏览器的本地存储中存储最后一个JSON格式的数据。这可以用作notepad++ / Sublime / VSCode JSON美化的替代方案。
                                </li>
                                <li>
                                    这个JSON在线格式化器也可以作为JSON Lint工作。
                                </li>
                                <li>
                                    使用自动开关打开或关闭自动更新进行美化。
                                </li>
                                <li>
                                    它使用$。parseJSON和JSON。stringify美化JSON，以便于人类阅读和分析。
                                </li>
                                <li>
                                    下载JSON，一旦它被创建或修改，它可以在notepad++， Sublime，或VSCode替代打开。
                                </li>
                                <li>
                                    JSON格式检查器有助于修复缺失的引号，点击设置图标，看起来像一个螺丝刀在编辑器的左边来修复格式。
                                </li>
                            </ul>

                            <h2>JSON简介</h2>
                            <p>
                                JSON是一种轻量级的数据交换格式。 易于人阅读和编写。同时也易于机器解析和生成。 它基于JavaScript Programming Language, Standard
                                ECMA-262 3rd Edition - December 1999的一个子集。 JSON采用完全独立于语言的文本格式，但是也使用了类似于C语言家族的习惯（包括C,
                                C++, C#, Java, JavaScript, Perl, Python等）。 这些特性使JSON成为理想的数据交换语言。
                            </p>

                            <h2>与其他格式的比较</h2>
                            <h3>XML</h3>
                            <p>
                                JSON与XML最大的不同在于XML是一个完整的标记语言，而JSON不是。这使得XML在程序判读上需要比较多的功夫。主要的原因在于XML的设计理念与JSON不同。XML利用标记语言的特性提供了绝佳的延展性（如XPath），在数据存储，扩展及高级检索方面具备对JSON的优势，而JSON则由于比XML更加小巧，以及浏览器的内置快速解析支持，使得其更适用于网络数据传输领域。
                            </p>
                            <h3>YAML</h3>
                            <p>
                                在功能和语法上，JSON 都是 YAML 语言的一个子集。特别是，YAML
                                1.2规范指定“任何JSON格式的文件都是YAML格式的有效文件"。最常见的YAML解析器也能够处理JSON。版本 1.2 之前的 YAML 规范没有完全涵盖
                                JSON，主要是由于 YAML 中缺乏本机 UTF-32 支持，以及对逗号分隔空格的要求;此外，JSON 规范还包括 /* */ 样式的注释。YAML
                                最重要的区别是语法扩展集，它们在 JSON 中没有类似物：关系数据支持：在 YAML
                                文档中，可以引用以前在文件/流中找到的锚点;通过这种方式，您可以表达递归结构。支持除基元之外的可扩展数据类型，如字符串、数字、布尔值等。支持带缩进的块语法;它允许您在不使用不必要的符号的情况下描述结构化数据：各种括号、引号等。
                            </p>
                            <h3>MessagePack</h3>
                            <p>
                                MessagePack比JSON更短小，快速。
                            </p>
                            <h3>格式化工具</h3>
                            <p>
                                JSON格式取代了XML给网络传输带来了很大的便利，但是却没有了XML的一目了然，尤其是JSON数据很长的时候，会让人陷入繁琐复杂的数据节点查找中。开发者可以通过在线JSON格式化工具，来更方便的对JSON数据进行节点查找和解析。
                            </p>

                            <h2>参考资料:</h2>
                            <ul>
                                <li>
                                    <a href="https://zh.wikipedia.org/wiki/JSON">https://zh.wikipedia.org/wiki/JSON</a>
                                </li>
                                <li>
                                    <a
                                        href="https://zhuanlan.zhihu.com/p/33792109">https://zhuanlan.zhihu.com/p/33792109</a>
                                </li>
                                <li>
                                    <a href="https://www.json.org/json-zh.html">https://www.json.org/json-zh.html</a>
                                </li>
                                <li>
                                    <a href="https://developer.mozilla.org/zh-CN/docs/Learn/JavaScript/Objects/JSON">https://developer.mozilla.org/zh-CN/docs/Learn/JavaScript/Objects/JSON</a>
                                </li>
                            </ul>

                        </div>
                        <div class="accordion-group"></div>
                    </div>
                </div>
            </div>
        </div>
        <div class="right">
            <div class="search">
                <input id="keyword" />
                <div class="search-btn">搜索</div>
            </div>
            <div class="recommend">
                <div class="recommend-head">相关推荐</div>
                <div class="recommend-list">
                    <a class="recommend-list-item" href="https://ps.gitapp.cn">在线ps</a>
                    <a class="recommend-list-item" href="https://fangdai.gitapp.cn">房贷计算器</a>
                    <a class="recommend-list-item" href="https://ps.fktool.com">Online PS</a>
                    <a class="recommend-list-item" href="https://base64.fktool.com">base64解码</a>
                </div>
            </div>
        </div>
    </div>

    <script src="./static/script/jquery-1.11.3.min.js" type="text/javascript"></script>
    <script src="./static/script/bootstrap.min.js" type="text/javascript"></script>
    <script src="./static/script/tool.js" type="text/javascript"></script>
    <script src="./static/script/json/jsonformat.js" type="text/javascript"></script>
    <script type="text/javascript">setJS(["./static/script/json/jsonzip.js"]);</script>
    </div>


    <div class="copyright" id="footer">
        <div class="container">
            <div class="row">
                <div class="col-sm-12">
                    <span>
                        Copyright ©2023
                        <a href="/">
                            fktool在线工具网
                        </a>
                    </span>
                    |
                    <span>
                    </span>
                </div>
            </div>
        </div>
    </div>

    <script>
    </script>

</body>

</html>
```

## 与其他格式比较

- XML
JSON与XML最大的不同在于XML是一个完整的标记语言，而JSON不是。这使得XML在程序判读上需要比较多的功夫。主要的原因在于XML的设计理念与JSON不同。XML利用标记语言的特性提供了绝佳的延展性（如XPath），在数据存储，扩展及高级检索方面具备对JSON的优势，而JSON则由于比XML更加小巧，以及浏览器的内置快速解析支持，使得其更适用于网络数据传输领域。

- YAML
在功能和语法上，JSON 都是 YAML 语言的一个子集。特别是，YAML 1.2规范指定“任何JSON格式的文件都是YAML格式的有效文件"。最常见的YAML解析器也能够处理JSON。版本 1.2 之前的 YAML 规范没有完全涵盖 JSON，主要是由于 YAML 中缺乏本机 UTF-32 支持，以及对逗号分隔空格的要求;此外，JSON 规范还包括 /* */ 样式的注释。YAML 最重要的区别是语法扩展集，它们在 JSON 中没有类似物：关系数据支持：在 YAML 文档中，可以引用以前在文件/流中找到的锚点;通过这种方式，您可以表达递归结构。支持除基元之外的可扩展数据类型，如字符串、数字、布尔值等。支持带缩进的块语法;它允许您在不使用不必要的符号的情况下描述结构化数据：各种括号、引号等。

- MessagePack
MessagePack比JSON更短小，快速。

## 总结

JSON格式取代了XML给网络传输带来了很大的便利，但是却没有了XML的一目了然，尤其是JSON数据很长的时候，会让人陷入繁琐复杂的数据节点查找中。开发者可以通过在线JSON格式化工具，来更方便的对JSON数据进行节点查找和解析。
