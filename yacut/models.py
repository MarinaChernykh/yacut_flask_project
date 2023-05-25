from datetime import datetime
import re

from flask import url_for
from sqlalchemy.orm import validates

from yacut import db
from .constants import SHORT_URL_PATTERN, SHORT_URL_MAX_SIZE


class URLMap(db.Model):
    """Содержит исходные ссылки и соответствующие им короткие."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @validates('original')
    def validate_original(self, key, url):
        """Проверяет корректность введенной длинной ссылки."""
        if not all((url, 1 <= len(url) <= 256)):
            raise ValueError('Указана недопустимая ссылка')
        return url

    @validates('short')
    def validate_short(self, key, short_url):
        """Проверяет корректность введенной короткой ссылки."""
        if not 1 <= len(short_url) <= SHORT_URL_MAX_SIZE:
            raise ValueError('Запись должна включать до 16 символов')
        if not re.fullmatch(SHORT_URL_PATTERN, short_url):
            raise ValueError('Допустимы только латинские буквы и цифры')
        return short_url

    def to_dict(self):
        """Создает словарь для API на основе экземпляра класса."""
        return dict(
            url=self.original,
            short_link=url_for("original_url_view", short=self.short, _external=True),
        )

    def from_dict(self, data):
        """Преобразует словарь, полученный от API, в аттрибуты экземпляра класса."""
        for model_field, api_field in (('original', 'url'), ('short', 'custom_id')):
            setattr(self, model_field, data[api_field])

    def create_record(self):
        """Создает в базе данных новую запись."""
        db.session.add(self)
        db.session.commit()
