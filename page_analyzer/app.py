"""
Flask application module for Page Analyzer.

This module defines the main Flask application and all route handlers
for the page analysis service. It provides endpoints for:
    - Home page with URL submission form
    - URL listing page
    - Individual URL details page
    - URL check creation endpoint

Routes:
    GET / - Home page with URL submission form
    POST / - Handle URL submission and validation
    GET /urls - Display list of all analyzed URLs
    GET /urls/<id> - Display details and checks for specific URL
    POST /urls/<id>/checks - Create new check for URL

Environment Variables:
    SECRET_KEY: Flask secret key for session management
    DATABASE_URL: PostgreSQL connection string (handled by models module)
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from .checker import check_url
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
    """
    Render the home page with URL submission form.

    Returns:
        str: Rendered HTML template for the home page
    """
    return render_template('index.html')


@app.post('/')
def add_url_route():
    """
    Handle URL submission from the home page form.

    Validates the submitted URL, checks for duplicates, and adds
    new URLs to the database. Displays appropriate flash messages
    for success, duplicate, or validation errors.

    Returns:
        Response: Redirect to URL details page on success,
                 or rendered template with error message
        int: HTTP status code (422 for validation errors, 500 for DB errors)
    """
    url = request.form.get('url', '').strip()

    is_valid, result = validate_url(url)

    if not is_valid:
        flash(result, 'danger')
        return render_template('index.html'), 422

    existing_url = get_url_by_name(result)
    if existing_url:
        flash('Страница уже существует!', 'info')
        return redirect(url_for('show_url', url_id=existing_url['id']))

    url_id = add_url(result)

    if url_id:
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url', url_id=url_id))
    else:
        flash('Ошибка при добавлении страницы', 'danger')
        return render_template('index.html'), 500


@app.route('/urls')
def show_urls():
    """
    Display list of all analyzed URLs with their last check information.

    Retrieves all URLs from the database along with their most recent
    check date and status code, sorted by ID in descending order
    (newest first).

    Returns:
        str: Rendered HTML template showing all URLs
    """
    urls = get_urls_with_last_check()
    return render_template('urls.html', urls=urls)


@app.route('/urls/<int:url_id>')
def show_url(url_id):
    """
    Display detailed information about a specific URL and its checks.

    Shows URL metadata and all associated checks with their results
    (status code, h1, title, description).

    Args:
        url_id (int): The ID of the URL to display

    Returns:
        Response: Redirect to URLs list if not found,
                 or rendered template with URL details and checks
    """
    url_data = get_url_by_id(url_id)

    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('show_urls'))

    checks = get_checks_by_url_id(url_id)
    return render_template('url.html', url_data=url_data, checks=checks)


@app.post('/urls/<int:url_id>/checks')
def create_check(url_id):
    """
    Create a new check for the specified URL.

    Performs an HTTP request to the URL, extracts SEO metadata
    (h1, title, description), and stores the results in the database.
    Only creates a check record if the HTTP request is successful.

    Args:
        url_id (int): The ID of the URL to check

    Returns:
        Response: Redirect to URL details page with flash message
                 indicating success or failure
    """
    url_data = get_url_by_id(url_id)

    if not url_data:
        flash('Страница не найдена', 'danger')
        return redirect(url_for('show_urls'))

    success, status_code, h1, title, description = check_url(
        url_data['name']
    )

    if success:
        check_id = add_check(
            url_id, status_code, h1, title, description
        )
        if check_id:
            flash('Страница успешно проверена', 'success')
        else:
            flash('Произошла ошибка при проверке', 'danger')
    else:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('show_url', url_id=url_id))
