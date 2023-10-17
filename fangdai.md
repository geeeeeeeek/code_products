# 【开源分享】基于Html开发的房贷计算器，模仿新浪财经
> 房贷计算器是一种房贷计算的在线计算Web应用，按用户选择的贷款类型、贷款金额、期限、利率可计算得出每月月供参考、支付利息、还款总额这些信息。本文模仿新浪财经开发的房贷计算器。


## 作品预览
https://fangdai.gitapp.cn

## 源码地址
https://github.com/geeeeeeeek/fangdai


## 代码结构

整个项目代码分为css、js、image和index.html ，总的来说，代码结构比较简单，容易理解。主入口文件就是index.html，感兴趣的同学可以下载代码学习。
![fd-code.jpg](https://upload-images.jianshu.io/upload_images/3360192-4b26ef5823db240e.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


各种css和js文件通过link的方式引入，如下：
```
<link rel="icon" sizes="114x114" href="images/favicon.png">
<link rel="stylesheet" type="text/css" href="/css/my-common.min.css"/>
<link rel="stylesheet" type="text/css" href="/css/my-houseloan.min.css"/>
<script type="text/javascript" src="/js/zepto.min.js" async></script>
<script type="text/javascript" src="/js/houseloan_calculator.js" async></script>
<script src="/js/common_tpl.js" type="text/javascript" async></script>
```

## 首页预览
![fd-index.jpg](https://upload-images.jianshu.io/upload_images/3360192-7b8759d24baa1b88.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



