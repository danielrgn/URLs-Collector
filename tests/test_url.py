from unittest import TestCase
import mock
from models.url import Url

url = Url('www.google.com.br')


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def text(self):
        return self.json_data


class UrlTests(TestCase):
    @staticmethod
    def test_set_url_with_sanitize():
        assert url.url == 'http://www.google.com.br'

    @mock.patch('requests.get')
    def test_get_urls_from_entry_url_mock_requests(self, mock_get):
        mock_resp = self._mock_response(
            text='<html><a href="http://www.google.com">Google</a>'
                 '<a href="https://gist.github.com">github</a></html>')
        mock_get.return_value = mock_resp

        resp = url.get_urls_from_entry_url()

        assert resp == ['http://www.google.com', 'https://gist.github.com']

    @staticmethod
    def _mock_response(text=""):
        mock_resp = mock.Mock()
        mock_resp.text = text
        return mock_resp
