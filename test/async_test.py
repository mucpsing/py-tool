import time, aiohttp, asyncio


async def multi_request(urls: list[str], params: list = list()) -> list:
    """
    @Description {description}

    - param urls             :{param} {description}
    - param params=list() :{list}  {description}

    @returns `{ list}` {description}
    @example
    ```py

    urls = ['https://1', 'https://2']
    params = []
    r = multi_request()
    asyncio.run()

    ```

    """
    tasks = []

    async def fetch_post(session, url, data):
        async with session.post(url, json=data) as response:
            if response.status != 200:
                response.raise_for_status()
            text = await response.text()
            return text

    async def fetch(session, url):
        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()
            text = await response.text()
            return text

    connector = aiohttp.TCPConnector(limit=200)
    # connector = aiohttp.TCPConnector(force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        # async with aiohttp.ClientSession() as session:
        if len(params) > 0:
            tasks = [
                asyncio.create_task(fetch_post(session, urls[i], params[i]))
                for i in range(len(urls))
            ]
        else:
            tasks = [asyncio.create_task(fetch(session, url)) for url in urls]

        responses = await asyncio.gather(*tasks)

    return responses


async def main(urls, params):
    start = time.time()
    res = await multi_request(urls, params)
    end = time.time()

    print("总耗时: ", round(end - start, 3))
    print(res)


if __name__ == "__main__":

    count = 10
    urls_get = [f"http://localhost:4040/test/get/{e}" for e in range(count)]
    urls_post = [f"http://localhost:4040/test/post" for e in range(count)]

    params = [{"request_str": str(e), "request_int": e} for e in range(count)]

    tasks = main(urls_post, params)
    asyncio.run(tasks)
