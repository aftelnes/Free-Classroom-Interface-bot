import config
from api._base import request

async def get_data(data_type: str) -> list:
    """Функция получения списка факеультетов или оснащения"""

    if data_type == 'FACULTIES_URL':
        url_endpoint = config.base_config.FACULTIES_URL
    elif data_type == 'EQUIPMENTS_URL':
        url_endpoint = config.base_config.EQUIPMENTS_URL
    elif data_type == 'LESSONS_NUM_URL':
        url_endpoint = config.base_config.LESSONS_NUM_URL

    response = await request(url=f"{config.base_config.SERV_URL}{url_endpoint}", method='get')
    return response