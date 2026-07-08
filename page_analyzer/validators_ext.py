import validators
from urllib.parse import urlparse


def validate_url(url):
    """
    Валидация URL.
    Возвращает кортеж (is_valid, normalized_url_or_error)
    """
    if not url:
        return False, "URL не может быть пустым"
    
    if len(url) > 255:
        return False, "URL не должен превышать 255 символов"
    
    if not validators.url(url):
        return False, "Некорректный URL"
    
    # Нормализация URL
    parsed = urlparse(url)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}"
    
    return True, normalized_url
