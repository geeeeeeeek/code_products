# 京东App秒杀抢购流程接口分析

App数据抓包必需工具
必需工具：小米手机，Charles，HttpCanary

从2021年2月后，京东只限于从app发起抢购，所以，网上的很多工具已经无效了。只能分析app端的底层协议和流程。

通过抓包可以发现，整个抢购流程分为七个步骤，如下：

1. 第一步是genToken ，这一步需要sign签名，charles抓包下来的sign签名是可以重复利用的，请求后获得Token与下一步需要跳转的url：

```
http://api.m.jd.com/client.action?functionId=genToken&clientVersion=10.1.2&build=89743&client=android&d_brand=OPPO&d_model=PCRT00&osVersion=5.1.1&screen=1920*1080&partner=lc023&oaid=&eid=eidAe81b812187s36z8QOkxpRJWzMceSvZJ6Ges/EbXnbK3TBxc/JEcutXxuELIRMJDVeTNJFcAF/+tx1qw9GllLTdSnFeV3ic6909a697SbDL9zxEc4&sdkVersion=22&lang=zh_CN&aid=21e9fa9db1e4e15d&area=19_1601_3633_63257&networkType=wifi&wifiBssid=unknown&uts=0f31TVRjBSsqndu4jgUPz6uymy50MQJw+3mGtYmx2hY8nVZkXFqGJ2D3wO8rvc+nAbe881zrDZjz3yU3z8vQgL8NZ7e39M3H2YpLER13q+3VUzHQXXLg4BMmeH+1W0+xQLR4Y58JMW9A9F9yD2BtQPynkeKYtBsYDCkOn35Tv9ci57mPbqxYWU0TDVJ8t7JBXRhLckTorzxtEAVucA==&uemps=0-0&harmonyOs=0&skuId=100012043978&sv=102&st=1639233570251&uuid=aa126fe5cf6dfc0a&sign=ef78cdeda16a5269f11d3fdf920e0b5e&body={"action":"to","to":"https://divide.jd.com/user_routing?skuId=100012043978"}
```

此处要注意，请求中的body一定要传：
```
{"action":"to","to":"https://divide.jd.com/user_routing?skuId=100012043978"}
```

请求后：
```
{
	"code": "0",
	"tokenKey": "AAEAMO6g-6W-wURCFfDn3vw7jvHvMfP_gGjoHwIwW_orBxjg62m844R-Urf4szuLvgfbDA1",
	"url": "https://un.m.jd.com/cgi-bin/app/appjmp"
}
```
2. 然后是appjmp步骤，请求链接为：https://un.m.jd.com/cgi-bin/app/appjmp，需要用到第一步中的tokenKey，请求后的response.headers：

```
location: https://divide.jd.com/user_routing?skuId=100012043978&mid=Ys6S3Ax2ML**********PS9MLCKdo&lng=109.568546&lat=33.999595&sid=470f133fa4**********9d6cf6bew
set-cookie: pt_key=app_open***********; EXPIRES=Thu, 17-Jun-2021 04:04:07 GMT; PATH=/; DOMAIN=.jd.com; HTTPONLY
set-cookie: pt_pin=aa**********; EXPIRES=Thu, 17-Jun-2021 04:04:07 GMT; PATH=/; DOMAIN=.jd.com; HTTPONLY
set-cookie: pwdt_id=aa**********; EXPIRES=Thu, 17-Jun-2021 04:04:07 GMT; PATH=/; DOMAIN=.jd.com
set-cookie: sid=470f133f**********; EXPIRES=Thu, 17-Jun-2021 04:04:07 GMT; PATH=/; DOMAIN=.jd.com
```

location中的url即为下一步跳转的链接，后面几步请求都需要带上这四个set cookie

3. divide 这一步也是get请求，完整的请求链接已经包含在第二步的response.headers[‘location’]中，请求后的response.headers：
```
Set-Cookie: seckillSku=100012043978;domain=divide.jd.com;path=/;expires=Tue, 18-May-21 04:06:07 GMT
Set-Cookie: seckillSid=470f133fa40**********6cf6bew;domain=divide.jd.com;path=/;expires=Tue, 18-May-21 04:06:07 GMT
Set-Cookie: mid=Ys6S3Ax2MLxvA91**********S9MLCKdo;domain=divide.jd.com;path=/;expires=Wed, 19-May-21 07:50:47 GMT
Location: https://marathon.jd.com/m/captcha.html?sid=470f133fa4**********d69d6cf6bew&lat=33.999595&mid=Ys6S3Ax2ML**********o2xFPS9MLCKdo&skuId=100012043978&lng=109.568546
```

location中的url即为下一步跳转的链接，这三个set cookie是不需要的。

4. captcha 验证，这一步成功的话就可以跳转到“填写订单”的页面，get请求后

```
location: https://marathon.jd.com/seckillM/seckill.action?skuId=100012043978&num=1&rid=1621310648
set-cookie: seckillSku=100012043978;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:06:08 GMT
set-cookie: seckillSid=470f1******************69d6cf6bew;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:06:08 GMT
set-cookie: mid=Ys6S3Ax2******************kPMgTjo2xFPS9MLCKdo;domain=marathon.jd.com;path=/;expires=Wed, 19-May-21 07:50:48 GMT
set-cookie: seckillSku=100012043978;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:06:08 GMT
set-cookie: seckillSid=;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:06:08 GMT
set-cookie: mid=Ys6S3Ax******************Tjo2xFPS9MLCKdo;domain=marathon.jd.com;path=/;expires=Wed, 19-May-21 07:50:48 GMT
set-cookie: seckill100012043978=wGPGg0Hl38hKCtL+qzDdnYtTACbdbHG4EHWZfrUevTmy91p9t9+FW1j25tuRKn/JUzz9kJndJuaQGu**********************************hPz+wKXOXNcWT0oP9/7aBzT6v51onNMwKNqL/oPq62tsnbn8hGgW;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:09:08 GMT
set-cookie: seckill100012043978=wGPGg0Hl38hKCtL+qzDdnYtTACbdbHG4EHWZfrUevTmy91p9t9+FW1j25tuRKn/JUzz9kJndJuaQGuZVd2z*****************************c8Zvh30ghPz+wKXOXNcWT0oP9/7aBzT6v51onNMwKNqL/oPq62tsnbn8hGgW;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:09:08 GMT
set-cookie: seckillSku=100012043978;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:06:08 GMT
set-cookie: seckillSid=;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:06:08 GMT
set-cookie: seckill100012043978=PQSX5FWmso33ZTy1qg3a59HQ/G3I4mZNiugB3jNblYyYsSjAqdcXmAtWIWizmwhWUHsfqEU1FzyruuESA/QMB6h25M*************************k2KrA8uJML5ClwGYMXV/JaCS9kfexcFQEYjzsErAwaF5Z3Q4zOOW+gjSRWTno/Z;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:09:08 GMT
```

location中出现
```
https://marathon.jd.com/seckillM/seckill.action?skuId=100012043978&num=1&rid=1621310648
```

代表验证成功，如果失败，则是：
```
https://marathon.jd.com/mobile/koFail.html
```

setcookie需要如下四个，后面的请求需要用到：
```
captcha_set_cookie = {
    'seckillSku': ,
    'seckillSid': '',
    'mid': ,
    'seckill100012043978': 'PQSX5FWmso33ZTy1qg3a59HQ/G3I4mZNiugB3jNblYyYsSjAqdcXmAtWIWizmwhWUHsfqEU1FzyruuESA/QMB6h25M*************************k2KrA8uJML5ClwGYMXV/JaCS9kfexcFQEYjzsErAwaF5Z3Q4zOOW+gjSRWTno/Z',
}
```

seckill100012043978在set cookie里重复出现，取最后一个即可。

5.  seckill.action请求，在app上就是填写订单，请求时需要带上captcha_set_cookie，如果请求成功，response.status_code为200，否则为302。需要说明的是，只有在抢购期间内才会请求成功，否则都是失败的，请求的response.headers为

```
set-cookie: seckillSku=100012043978;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:06:08 GMT
set-cookie: seckillSid=;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:06:08 GMT
set-cookie: seckillSku=100012043978;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:06:08 GMT
set-cookie: seckillSid=;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:06:08 GMT
set-cookie: seckill100012043978=+VxYCzRv8e9cKXdrgi***************************************z+wM0aVOm5AxZPjcq9CVPN3dmtUb73KdQOMbVCYrU/jZUvFE0WYNNz3DmvYjFaA8CmLY/SEYUyjyZrOMZSk2L/VdkA9AAydRRfNEM0Cj;domain=marathon.jd.com;path=/;expires=Tue, 18-May-21 04:09:08 GMT
content-language: zh-CN
```

这一步会拿到新的seckill100012043978数值，对应的cookie值需要更新。

6. init.action post类型，需要提交的数据charles都可以抓到， url为
```
https://marathon.jd.com/seckillnew/orderService/
```

7. 提交订单，post类型，需要提交的数据charles都可以抓到，url为
```
https://marathon.jd.com/seckillnew/orderService/submitOrder.action?skuId=100012043978
```

提交后返回：
```
{"errorMessage":"很遗憾没有抢到，再接再厉哦。","orderId":0,"resultCode":90016,"skuId":0,"success":false}
```
至此分析流程结束。

祝各位都能够抢到自己心仪的商品，技术交流可联系q：285126081



