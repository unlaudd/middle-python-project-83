"""
URL validation and normalization utilities.

This module provides functions to validate and normalize URLs before
storing them in the database. It ensures URLs are properly formatted
and extracts the base URL (scheme + netloc) for consistency.
"""

import validators
from urllib.parse import urlparse


def validate_url(url):
    """
    Validate and normalize a URL.

    Checks if the URL is non-empty, within length limits, and properly
    formatted. If valid, normalizes it to scheme + netloc format.

    Args:
        url (str): The URL string to validate.

    Returns:
        tuple: A tuple containing:
            is_valid (bool): True if URL is valid, False otherwise.
            result (str): Normalized URL if valid, or error message if invalid.

    Examples:
        >>> validate_url("https://example.com/path")
        (True, "https://example.com")

        >>> validate_url("")
        (False, "URL не может быть пустым")

        >>> validate_url("not-a-url")
        (False, "Некорректный URL")
    """
    try:
        if not url:
            return False, "URL не может быть пустым"

        if len(url) > 255:
            return False, "URL не должен превышать 255 символов"

        if not validators.url(url):
            return False, "Некорректный URL"

        # Normalize URL to scheme + netloc
        parsed = urlparse(url)
        normalized_url = f"{parsed.scheme}://{parsed.netloc}"

        return True, normalized_url

    except Exception:
        return False, "Некорректный URL"
