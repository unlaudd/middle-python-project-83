"""
Page Analyzer - A web application for SEO analysis of URLs.

This package provides a Flask-based web application that allows users
to analyze web pages for SEO optimization. It checks page availability,
extracts metadata (title, h1, description), and stores analysis results.

The main Flask application instance is exported as 'app' and can be
imported directly from this package:

    from page_analyzer import app

Usage:
    Development:
        $ make dev
    
    Production:
        $ make start

Configuration:
    The application requires the following environment variables:
        - SECRET_KEY: Flask secret key for session signing
        - DATABASE_URL: PostgreSQL connection string
"""

from .app import app

__all__ = ['app']
