import requests

async def shorten_url(url):
    try:
        shorten_url_api = 'https://smolurl.com/api/links'
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.post(shorten_url_api, json={'url': url}, headers=headers)
        return response.json()['data']['short_url']
    except (requests.exceptions.RequestException, KeyError):
        return url
