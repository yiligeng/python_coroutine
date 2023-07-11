'''
@Project ：python_coroutine 
@File    ：image_download.py
@Author  ：gyl
@Date    ：2023/7/11 11:07 AM 
'''
import asyncio

import aiofiles
import aiohttp

"""
使用async和await关键字，我们可以编写出看起来像同步代码的异步代码。
在这种代码中，异步操作（如网络请求）的等待不再需要使用回调函数或者其他特殊的控制结构，
而是直接使用await关键字。当程序遇到await关键字时，
它会“暂停”当前的协程，将控制权交回到事件循环，然后去执行其他的协程。
当异步操作完成时，程序会“恢复”被暂停的协程，继续执行后面的代码。
这样，我们就可以像写同步代码一样来写异步代码，使得代码的阅读和理解变得更简单。
"""


async def download_image(session, url):
    async with session.get(url) as response:
        # 假设URL的最后一部分是文件名
        filename = url.split("/")[-1]
        async with aiofiles.open(filename, 'wb') as f:
            """
            有两个 await 关键字，第一个是等待从网络响应中读取数据，
            第二个是等待把数据写入到文件中。这两个操作都是异步的，
            它们可能会花费一些时间。使用 await 关键字，
            我们可以在等待这些操作的时候，去执行其他的任务"""
            await f.write(await response.read())


async def main():
    # URL列表，每个URL指向一个图片
    urls = ['https://static.runoob.com/images/demo/demo2.jpg', 'https://static.runoob.com/images/demo/demo3.jpg']

    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, url) for url in urls]
        """
        asyncio.gather函数接受一系列的协程，然后返回一个新的协程，
        这个新的协程会等待传入的所有协程完成。这里使用了await关键字来运行这个协程，
        这样，所有的图片都会并发地下载，而不是一个接一个地下载。"""
        await asyncio.gather(*tasks)


# Python 3.7 及以后,不需要显式声明事件循环,可以使用 asyncio.run()来代替后的启动操作
asyncio.run(main())
