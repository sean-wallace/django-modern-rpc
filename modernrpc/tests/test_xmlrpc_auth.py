# coding: utf-8
import pytest
from django.utils.six.moves import xmlrpc_client


def test_user_logged(live_server, django_user_model):

    django_user_model.objects.create_user('johndoe', email='jd@example.com', password='123456')

    orig_url = live_server.url + '/all-rpc/'
    auth_url = orig_url.replace('http://', 'http://johndoe:123456@')

    client = xmlrpc_client.ServerProxy(auth_url)
    assert client.method_need_login(5) == 25

    with pytest.raises(xmlrpc_client.ProtocolError):
        client = xmlrpc_client.ServerProxy(orig_url)
        client.method_need_login(4)
