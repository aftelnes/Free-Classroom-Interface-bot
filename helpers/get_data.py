import config
from api._base import request

async def get_data(data_type: str, params=None) -> list:
    """Функция получения списка факеультетов или оснащения"""

    if data_type == 'FACULTIES':
        url_endpoint = config.base_config.FACULTIES_URL
    elif data_type == 'EQUIPMENTS':
        url_endpoint = config.base_config.EQUIPMENTS_URL
    elif data_type == 'LESSONS_NUM':
        url_endpoint = config.base_config.LESSONS_NUM_URL
    elif data_type == 'FREE_PLACES':
        url_endpoint = config.base_config.FREE_PLACES_URL

    response = await request(url=f"{config.base_config.SERV_URL}{url_endpoint}", method='get', params=params)
    return response