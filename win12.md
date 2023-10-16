> 据 MSPoweruser 报道，Windows 11虽然刚刚开始步入正轨，但最新爆料称微软已经在开启下一个计划，Windows 12 的开发将在 去年3 月份开始。德国科技网站 Deskmodder.de 称，根据内部消息，微软将在 2022年3 月开始开发 Windows 12 系统，尽管 Windows 11 正式版才在去年 10 月份发布。即使 Windows 12 很快进入开发阶段，我们也可能要等待相当长的一段时间，才会迎来微软的官方宣布，毕竟一款系统的开发需要多年的时间。


## 个人体验

不得不说，windows的更新进度太快了，记得当年上大学的时候，大家用的还是windows xp，之后是windows 7，然后没有经历windows10，现在直接是windwos11。据说微软的系统版本有个特点，就是隔代胜出。比如win xp和win7之间的vista，还有win7和win10之间的win8，都失败了。不知道win12是否能成功。

以下就是win12的体验界面

![win12体验界面](https://upload-images.jianshu.io/upload_images/3360192-bdcb8d56f7ce43d7.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

体验地址：https://win12.gitapp.cn

本网页是基于第三方开源项目https://github.com/tjy-gitnub/win12开发的，

## 开发要点

整个项目的开发是基于html5+jquery+javascript+css实现的，目前实现的功能包括：
-  基本功能与应用
-  外观整体优化
-  加入特效
-  窗口功能
 - 应用完善
 - 添加更多个性化方面的设置
 - 添加 Edge 应用
 - 为更多应用添加标签页
-  完善小组件，添加到桌面等功能
-  动态壁纸

## 代码结构

该项目结构共分为9个文件夹和主入口文件desktop.html和boot.html。代码结构如下图所示。其中，scripts文件夹包含了所有的js文件，media文件夹包含了所有的音频文件，比如开机启动音乐；img文件夹包含了所有的静态图片。

![src-win12.png](https://upload-images.jianshu.io/upload_images/3360192-196ca54d3bb677f1.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


## 关键代码

启动流程是先进入到boot.html，然后进入到desktop.html。

desktop.html关键代码如下：
```
<head>
	<meta charset="UTF-8" />
	<meta http-equiv="X-UA-Compatible" content="IE=edge" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
	<meta name="format-detection" content="telephone=no" />
 
	<link rel="stylesheet" href="./desktop.css">
	<link rel="stylesheet" href="bootstrap-icons.css">
	<!-- Apps style -->
	<link rel="stylesheet" href="apps/style/setting.css">
	<link rel="stylesheet" href="apps/style/explorer.css">
	<link rel="stylesheet" href="apps/style/calc.css">
	<link rel="stylesheet" href="apps/style/about.css">
	<link rel="stylesheet" href="apps/style/notepad.css">
	<link rel="stylesheet" href="apps/style/terminal.css">
	<link rel="stylesheet" href="apps/style/edge.css">
	<link rel="stylesheet" href="apps/style/camera.css">
	<link rel="stylesheet" href="apps/style/pythonEditor.css">
	<link rel="stylesheet" href="apps/style/run.css">
	<link rel="stylesheet" href="apps/style/whiteboard.css">
	<link rel="stylesheet" href="apps/style/defender.css">
	<link rel="stylesheet" href="apps/style/taskmgr.css">
	<link rel="stylesheet" href="widgets.css">
	<!-- 掌声欢迎 Copilot 的 css 引入(bs -->
	<link rel="stylesheet" href="apps/style/copilot.css">
	<link rel="manifest" href="pwa/manifest.json">
	<link rel="shortcut icon" href="./pwa/logo.png" type="image/x-icon">
	<link rel="stylesheet" href="apps/style/login.css">
	<!-- 各个模块 -->
	<link rel="stylesheet" href="module/tab.css">
	<base target="_blank">

	<title>Windows 12 网页版</title>
	<meta name="description" content="Windows 12网页版是一个在线体验Windows 12操作系统的开源项目,使用 HTML、CSS 和 JavaScript 模拟 Windows 12 操作系统的界面与交互。">
	<meta name="keywords" content="Windows 12, Windows 12网页版, 在线Windows 12">
	<meta name="keywords" content="Windows 12, Windows 12网页版, 在线Windows 12">
</head>
```

## 部署运行（nginx）

将代码下载到本地后，在D盘新建文件夹html，然后将源码放到里面，然后配置nginx的html根目录即可。nginx配置如下：

```
    server {
        listen       80;
        server_name  localhost;

        location / {
            root   D:\html; // 你的代码目录
            index  desktop.html;
	    try_files $uri $uri/ /desktop.html;
        }
    }
    
```
然后浏览器访问 localhost即可


## 参考知识

- [github的desktop页面写法](https://github.com/geeeeeeeek/win12/blob/main/desktop.html)
- [javascript学习教程](https://developer.mozilla.org/zh-CN/docs/Learn/JavaScript/First_steps/What_is_JavaScript)
- [CSS学习教程](https://developer.mozilla.org/zh-CN/docs/Learn/CSS)
- [html学习教程](https://www.w3cschool.cn/html/)
- [基于jquery开发的Windows 12网页版](https://zhuanlan.zhihu.com/p/658336845)

