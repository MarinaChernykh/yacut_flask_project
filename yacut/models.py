from datetime import datetime

from flask import url_for

from yacut import db


class URLMap(db.Model):
    """Содержит исходные ссылки и соответствующие им короткие."""
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

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
