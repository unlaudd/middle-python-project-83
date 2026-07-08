import requests
from bs4 import BeautifulSoup


def check_url(url):
    """
    Выполнить проверку URL.
    Возвращает кортеж (success, status_code, h1, title, description)
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
