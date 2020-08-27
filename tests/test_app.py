from flask import json


data_created_mock = {'entry_url': 'http://google.com.br',
                     'url_list': ['http://schema.org/WebPage',
                                  'http://www.google.com.br/imghp?hl=pt-BR&tab=wi'],
                     '_id': 'b47a42f70fecbbde1ffe79c883eea066'}

get_doc_mock = {'entry_url': 'http://google.com.br',
                'url_list': ['http://schema.org/WebPage',
                             'http://www.google.com.br/imghp?hl=pt-BR&tab=wi'],
                '_id': 'a72a42f70fecbbde1ffe79c883eeaA8d', }


def test_get_route_deafult_status_code_success(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.content_type == 'text/html; charset=utf-8'


def test_get_url_by_id_doc_return_none(client, mocker):
    mocker.patch('app._url_collector', return_value=data_created_mock)
    mocker.patch('settings.database.get_document', return_value=None)

    res = client.get('/api/urls/a72a42f70fecbbde1ffe79c883eeaA8d')

    assert res.json is False
    assert res.status_code == 200


def test_get_url_by_id_url_collector_return_none(client, mocker):
    mocker.patch('app._url_collector', return_value=None)
    mocker.patch('settings.database.get_document', return_value=get_doc_mock)

    res = client.get('/api/urls/b47a42f70fecbbde1ffe79c883eea066')

    assert res.json == []
    assert res.status_code == 200


def test_get_url_by_id_url_collector_success(client, mocker):
    mocker.patch('app._url_collector', return_value=data_created_mock)
    mocker.patch('settings.database.get_document', return_value=get_doc_mock)

    res = client.get('/api/urls/b47a42f70fecbbde1ffe79c883eea066')
    expected = [['http://schema.org/WebPage', 'http://www.google.com.br/imghp?hl=pt-BR&tab=wi'],
                ['http://schema.org/WebPage', 'http://www.google.com.br/imghp?hl=pt-BR&tab=wi']]

    assert len(res.json) == 2
    assert len(res.json[0]) == 2
    assert len(res.json[1]) == 2
    assert res.json == expected
    assert res.json[0] == expected[0]
    assert res.json[1] == expected[1]
    assert res.status_code == 200


def test_post_url_success(client, mocker):
    mocker.patch('models.url.Url.get_urls_from_entry_url',
                 return_value=data_created_mock['url_list'])
    res = client.post('/api/urls',
                      data=json.dumps({'url': 'google.com.br'}),
                      content_type='application/json')

    assert res.json['entry_url'] == 'http://google.com.br'
    assert len(res.json['url_list']) == 2
    assert res.json['url_list'][0] == 'http://schema.org/WebPage'
    assert res.json['url_list'][1] == 'http://www.google.com.br/imghp?hl=pt-BR&tab=wi'
    assert res.status_code == 200


def test_post_url_collector_return_none(client):
    res = client.post('/api/urls',
                      data=json.dumps({'url': 'google.com.br]'}),
                      content_type='application/json')

    assert res.json == 'Error collecting URLs: google.com.br]'
    assert res.status_code == 200


def test_post_url_with_param_invalid_success(client):
    res = client.post('/api/urls',
                      data=json.dumps({'urls': 'google.com.br'}),
                      content_type='application/json')

    assert res.json == []
    assert res.status_code == 200
