import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
from ACEest_Fitness import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b'ACEest' in res.data

def test_health(client):
    res = client.get('/health')
    assert res.status_code == 200
    assert res.get_json()['status'] == 'healthy'

def test_get_members_empty(client):
    res = client.get('/members')
    assert res.status_code == 200
    assert res.get_json()['count'] == 0

def test_add_member(client):
    res = client.post('/members', json={"name": "Rahul", "email": "rahul@gym.com", "plan": "premium"})
    assert res.status_code == 201
    assert res.get_json()['member']['name'] == 'Rahul'

def test_add_member_missing_fields(client):
    res = client.post('/members', json={"name": "NoEmail"})
    assert res.status_code == 400

def test_get_classes(client):
    res = client.get('/classes')
    assert res.status_code == 200
    assert len(res.get_json()['classes']) == 3

def test_book_class(client):
    res = client.post('/classes/1/book')
    assert res.status_code == 200

def test_book_invalid_class(client):
    res = client.post('/classes/999/book')
    assert res.status_code == 404