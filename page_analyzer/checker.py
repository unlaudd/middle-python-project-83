"""
URL checker and SEO metadata extractor.

This module provides functionality to fetch web pages and extract
basic SEO-related metadata such as the page title, main heading (h1),
and meta description. It handles network errors gracefully.
"""

import requests
from bs4 import BeautifulSoup


def check_url(url):
    """
    Fetch a URL and extract SEO metadata.

    Performs an HTTP GET request to the specified URL and parses
    the HTML response to extract the title, h1 tag, and meta
    description.

    Args:
        url (str): The URL to check and analyze.

    Returns:
        tuple: A tuple containing:
            success (bool): True if the request was successful (2xx).
            status_code (int): HTTP response code, or None on error.
            h1 (str): Text of the first h1 tag, or None.
            title (str): Text of the title tag, or None.
            description (str): Content of meta description, or None.
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else None

        h1_tag = soup.find('h1')
        h1 = h1_tag.get_text(strip=True) if h1_tag else None

        description_tag = soup.find(
            'meta', attrs={'name': 'description'}
        )
        description = None
        if description_tag:
            description = description_tag.get('content', '').strip()
            if not description:
                description = None

        return True, response.status_code, h1, title, description

    except requests.exceptions.RequestException:
        return False, None, None, None, None
