import re
import requests


class Url:
    def __init__(self, url):
        self.url = self._sanitize_url(url)
    
    def get_urls_from_entry_url(self):
        try:
            f = requests.get(self.url)
            urls = self._get_urls_from_string(f.text)
        except Exception as ex:
            urls = None
        return urls

    @staticmethod
    def _get_urls_from_string(text):
        regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.findall(regex, text)

    @staticmethod
    def _sanitize_url(url):
        return url if 'http://' in url or 'https://' in url else 'http://' + url
