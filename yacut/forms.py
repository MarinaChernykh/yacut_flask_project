from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import SHORT_URL_PATTERN, SHORT_URL_MAX_SIZE


class URLMapForm(FlaskForm):
    """Форма для ввода полной ссылки и создания короткой."""
    original_link = URLField(
        'Длинная ссылка',
        validators=(
            DataRequired(message='Обязательное поле'),
            Length(
                min=1, max=256,
                message='Запись не должна превышать 256 символов'
            )
        )
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(
            Length(
                min=1, max=SHORT_URL_MAX_SIZE,
                message='Запись должна включать от 6 до 16 символов'
            ),
            Regexp(
                SHORT_URL_PATTERN,
                message='Допустимы только латинские буквы и цифры'
            ),
            Optional()
        )
    )
    submit = SubmitField('Создать')
