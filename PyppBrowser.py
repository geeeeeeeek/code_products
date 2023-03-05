import asyncio
import os
import sys
import time
from pyppeteer import launch


class PyppBrowser:

    def __init__(self):
        self.base_path = os.getcwd()

        self.sec_url = ''
        self.cookie_dict = None
        self.userAgent = 'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.106 Mobile Safari/537.36'
        self.browser = None
        self.page = None
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.init_page())

    async def init_page(self):
        if self.browser is None:
            browser = await launch({'headless': True, 'dumpio': True, 'autoClose': False,
                                    'args': [
                                        '--no-sandbox',
                                        '--window-size=1920,1080',
                                        '--hide-scrollbars',
                                        '--start-maximized',  # 最大化窗口
                                        '--disable-infobars']
                                    })
            self.browser = browser
            if self.page is None:
                page = await self.browser.newPage()  # 打开新的标签页
                await page.emulateMedia('screen')
                await page.setViewport(viewport={"width": 480, "height": 800, "isMobile": True, 'hasTouch': True})
                await page.setCacheEnabled(True)
                await page.setJavaScriptEnabled(True)
                self.page = page

    async def _response(self, resp):
        if 'submitOrder.action' in resp.url:
            print('resp---->' + resp.url)
            resp_json = await resp.json()
            try:
                print(str(resp_json))
            except Exception as e:
                print(str(e))

    async def jump_page(self, url):
        await self.page.setUserAgent(self.userAgent)
        try:
            # 访问302跳转页面
            start = int(time.time() * 1000)
            self.page.on("response", lambda resp: asyncio.ensure_future(self._response(resp)))
            res = await self.page.goto(url)
            end = int(time.time() * 1000)
            print("goto耗时：" + str(end - start))
            selector = '.submit-btn'
            # 等待"提交订单"按钮
            await self.page.waitForSelector(selector=selector, options={'timeout': 3000})
            await self.page.click(selector=selector, options={'clickCount': 1})
            await self.page.screenshot(
                {'path': self.base_path + os.sep + str(int(time.time() * 1000)) + '.jpg', 'quality': 90,
                 'fullPage': True})  # 截图保存路径
        except Exception as e:
            print(str(e))
        finally:
            await self.browser.close()

    def jump(self, url):
        self.loop.run_until_complete(self.jump_page(url))
        return self.sec_url, self.cookie_dict


if __name__ == '__main__':

    # 跳转链接，把跳转链接扔进pypp即可
    url = 'https://un.m.jd.com/cgi-bin/app/appjmp?tokenKey=AAEAIK0eJgVbAoFuRh0JO_DEXpCXyW8s0i-WkbAjGUrmvEIh1&to=https%3A%2F%2Fdivide.jd.com%2Fuser_routing%3FskuId%3D100018466614%26from%3Dapp'
    pyppBrowser = PyppBrowser()
    pyppBrowser.jump(url)
