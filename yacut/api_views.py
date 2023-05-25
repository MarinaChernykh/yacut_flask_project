import re
from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id
from .constants import SHORT_URL_PATTERN, SHORT_URL_MAX_SIZE


@app.route('/api/id/', methods=('POST',))
def create_url():
    """Создает и сохраняет короткую версию ссылки."""
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] in (None, ''):
        data['custom_id'] = get_unique_short_id()
    else:
        if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
            raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
        if not all((
            re.fullmatch(SHORT_URL_PATTERN, data['custom_id']),
            len(data['custom_id']) <= SHORT_URL_MAX_SIZE
        )):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url = URLMap()
    url.from_dict(data)
    url.create_record()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_url(short_id):
    """Возвращает полную версию ссылки."""
    url = URLMap.query.filter_by(short=short_id).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original}), HTTPStatus.OK
