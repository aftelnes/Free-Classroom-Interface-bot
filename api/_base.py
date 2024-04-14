"""
Модуль запросов к API server
"""

from aiohttp import ClientSession

async def request(url: str, method: str, headers: dict = None, params: dict = None):
    async with ClientSession() as session:
        try:
            async with getattr(session, method)(url, params=params, headers=headers) as response:
                data = await response.json()
                return data
        except Exception as error:
            print('request Error = ', error)

