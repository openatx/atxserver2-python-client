# coding: utf-8
#

import pytest
import atxserver2


@pytest.fixture
def client():
    return atxserver2.Client("http://localhost:4000",
                             "97076434bbbe4dcfb176715e3cad766f")


def test_user(client: atxserver2.Client):
    info = client.user_info()
    assert "username" in info
    assert "email" in info


def test_list_device(client: atxserver2.Client):
    for d in client.list_device():
        d._udid = "xxx"
        d.acquire()
        print(d.atx_agent_address)
        print(d.remote_connect_address)
        d.release()


def test_aquire_device(client: atxserver2.Client):
    assert len(client.list_device()) > 0, "test prepare is not ready, device list is empty"
    for d in client.list_device():
        d.acquire(6000)
        info = d.info
        d.release()
        assert info['idleTimeout'] == 6000
        assert info['using'] == True
        break

    