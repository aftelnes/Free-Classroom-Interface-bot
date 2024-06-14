import config
from api._base import request


async def get_data(endpoint: str, params=None) -> list:
    """Функция получения списка факеультетов или оснащения"""

    response = await request(
        url=f"{config.base_config.SERV_URL}{endpoint}",
        method='get',
        params=params
    )
    return response
