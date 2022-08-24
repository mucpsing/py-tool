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
        async with session.post(url, data) as response:
            if response.status != 200:
                response.raise_for_status()
            data = await response.text()
            return data

    async def fetch(session, url):
        async with session.get(url) as response:
            if response.status != 200:
                response.raise_for_status()
            data = await response.text()
            return data

    async with aiohttp.ClientSession() as session:
        if len(params) > 0:
            tasks = [
                asyncio.create_task(fetch(session, urls[i], params[i]))
                for i in range(len(urls))
            ]
        else:
            tasks = [asyncio.create_task(fetch(session, url)) for url in urls]

        responses = await asyncio.gather(*tasks)

    return responses


async def main(urls):
    start = time.time()
    res = await multi_request(urls)
    end = time.time()

    print("总耗时: ", round(end - start, 3))
    print(res)


if __name__ == "__main__":

    count = 10
    urls = [f"http://localhost:4040/test/post" for e in range(count)]
    print("urls: ", urls)
    params = [{"request_str": str(e), "request_int": e} for e in range(count)]
    print("params: ", params)

    tasks = main(urls)
    asyncio.run(tasks)
