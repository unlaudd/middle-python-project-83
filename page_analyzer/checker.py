import requests


def check_url(url):
    """
    Выполнить проверку URL.
    Возвращает кортеж (success, status_code)
    """
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return True, response.status_code
    except requests.exceptions.RequestException:
        return False, None
