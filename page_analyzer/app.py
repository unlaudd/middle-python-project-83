import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from .models import (
    add_url,
    get_url_by_id,
    get_url_by_name,
    add_check,
    get_checks_by_url_id,
    get_urls_with_last_check,
)
from .validators_ext import validate_url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'super_secret_default_key')


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/')
def add_url_route():
    """Обработчик добавления URL"""
    url = request.form.get('url', '').strip()

    is_valid, result = validate_url(url)

    if not is_valid:
        flash(result, 'danger')
        return render_template('index.html'), 422

    # Проверяем, существует ли уже такой URL
    existing_url = get_url_by_name(result)
    if existing_url:
        flash('Страница уже существует!', 'info')
        return redirect(url_for('show_url', url_id=existing_url['id']))

    # Добавляем URL
    url_id = add_url(result)

    if url_id:
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url', url_id=url_id))
    else:
        flash('Ошибка при добавлении страницы', 'danger')
        return render_template('index.html'), 500


@app.route('/urls')
def show_urls():
    """Показать все URL"""
    urls = get_urls_with_last_check()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:url_id>')
def show_url(url_id):
    """Показать информацию о конкретном URL"""
    url_data = get_url_by_id(url_id)

    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('show_urls'))

    checks = get_checks_by_url_id(url_id)
    return render_template('url.html', url_data=url_data, checks=checks)


@app.post('/urls/<int:url_id>/checks')
def create_check(url_id):
    """Создать проверку для URL"""
    url_data = get_url_by_id(url_id)

    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('show_urls'))

    check_id = add_check(url_id)

    if check_id:
        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('show_url', url_id=url_id))
