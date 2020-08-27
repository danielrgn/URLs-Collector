from models.url import Url
from flask import json
import app

data_created_mock = {'entry_url': 'http://google.com.br',
                     'url_list': ['http://schema.org/WebPage', 'http://www.google.com.br/imghp?hl=pt-BR&tab=wi'],
                     '_id': 'b47a42f70fecbbde1ffe79c883eea066'}

get_doc_mock = {'entry_url': 'http://google.com.br',
                'url_list': ['http://schema.org/WebPage', 'http://www.google.com.br/imghp?hl=pt-BR&tab=wi'],
                '_id': 'a72a42f70fecbbde1ffe79c883eeaA8d', }


def test_get_route_deafult_status_code_success(client):
    res = client.get('/')
    assert 200 == res.status_code
    assert 'text/html; charset=utf-8' == res.content_type


def test_get_url_by_id_doc_return_none(client, mocker):
    mocker.patch('app._url_collector', return_value=data_created_mock)
    mocker.patch('settings.database.get_document', return_value=None)

    res = client.get('/api/urls/a72a42f70fecbbde1ffe79c883eeaA8d')

    assert res.json is False
    assert 200 == res.status_code


def test_get_url_by_id_url_collector_return_none(client, mocker):
    mocker.patch('app._url_collector', return_value=None)
    mocker.patch('settings.database.get_document', return_value=get_doc_mock)

    res = client.get('/api/urls/b47a42f70fecbbde1ffe79c883eea066')

    assert [] == res.json
    assert 200 == res.status_code


def test_get_url_by_id_url_collector_return_none(client, mocker):
    mocker.patch('app._url_collector', return_value=data_created_mock)
    mocker.patch('settings.database.get_document', return_value=get_doc_mock)

    res = client.get('/api/urls/b47a42f70fecbbde1ffe79c883eea066')
    expected = [['http://schema.org/WebPage', 'http://www.google.com.br/imghp?hl=pt-BR&tab=wi'],
                ['http://schema.org/WebPage', 'http://www.google.com.br/imghp?hl=pt-BR&tab=wi']]

    assert 2 == len(res.json)
    assert 2 == len(res.json[0])
    assert 2 == len(res.json[1])
    assert expected == res.json
    assert expected[0] == res.json[0]
    assert expected[1] == res.json[1]
    assert 200 == res.status_code


def test_put_url_success(client, mocker):
    mocker.patch('app._url_collector', return_value=data_created_mock)
    res = client.post('/api/urls',
                      data=json.dumps({'url': 'google.com.br'}),
                      content_type='application/json')

    assert 'http://google.com.br' == res.json['entry_url']
    assert 2 == len(res.json['url_list'])
    assert 'http://schema.org/WebPage' == res.json['url_list'][0]
    assert 'http://www.google.com.br/imghp?hl=pt-BR&tab=wi' == res.json['url_list'][1]
    assert 'b47a42f70fecbbde1ffe79c883eea066' == res.json['_id']
    assert 200 == res.status_code


def test_put_url_collector_return_none(client, mocker):
    mocker.patch('app._url_collector', return_value=None)
    res = client.post('/api/urls',
                      data=json.dumps({'url': 'google.com.br'}),
                      content_type='application/json')

    assert 'Error collecting URLs: google.com.br' == res.json
    assert 200 == res.status_code


def test_put_url_with_param_invalid_success(client, mocker):
    res = client.post('/api/urls',
                      data=json.dumps({'urls': 'google.com.br'}),
                      content_type='application/json')

    assert [] == res.json
    assert 200 == res.status_code


def test_get_urls_from_entry_url(mocker):
    mocker.patch('models.url.Url.get_urls_from_entry_url', return_value=['http://google.com.br'])
    mocker.patch('settings.database.create_document', return_value=data_created_mock)

    url = Url('google.com.br')

    resp = app._url_collector(url.url)

    assert 'http://google.com.br' == resp['entry_url']
    assert ['http://schema.org/WebPage', 'http://www.google.com.br/imghp?hl=pt-BR&tab=wi'] == resp['url_list']
    assert 'b47a42f70fecbbde1ffe79c883eea066' == resp['_id']
    assert 2 == len(resp['url_list'])


def test_get_urls_from_entry_url_with_exception(mocker):
    mocker.patch('settings.database.create_document', return_value=data_created_mock)

    url = Url('google.com.br[')
    resp = app._url_collector(url.url)

    assert resp is None
