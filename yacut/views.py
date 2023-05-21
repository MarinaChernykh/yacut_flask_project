from string import ascii_letters, digits
from random import sample

from flask import flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .constants import SHORT_URL_MIN_SIZE


@app.route('/', methods=('GET', 'POST'))
def index_view():
    """Создает и сохраняет короткую версию ссылки."""
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
        elif URLMap.query.filter_by(short=short).first():
            flash(f'Имя {short} уже занято!', '')
            return render_template('index.html', form=form)
        url = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url)
        db.session.commit()
        flash('Ваша новая ссылка готова', url_for("original_url_view", short=short, _external=True))
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def original_url_view(short):
    """
    Переадресует по адресу полной ссылки на основе введенной короткой.
    """
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)


def get_unique_short_id():
    """Создает строку из 6 рандомных букв и цифр."""
    is_created = False
    while not is_created:
        short = ''.join(sample(ascii_letters + digits, SHORT_URL_MIN_SIZE))
        if URLMap.query.filter_by(short=short).first() is None:
            is_created = True
    return short
