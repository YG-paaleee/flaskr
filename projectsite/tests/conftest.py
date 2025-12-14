from pathlib import Path
from time import time
import pytest
import sys
import os
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from projectsite import create_app
from projectsite.db import get_db

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'MYSQL_HOST': os.environ.get('MYSQL_HOST', 'localhost'),
        'MYSQL_USER': os.environ.get('MYSQL_USER', 'root'),
        'MYSQL_PASSWORD': os.environ.get('MYSQL_PASSWORD', 'root'),
        'MYSQL_DB': os.environ.get('MYSQL_DB', 'psu'),
        'MYSQL_CURSORCLASS': os.environ.get('MYSQL_CURSORCLASS', 'DictCursor'),
        'JWT_SECRET_KEY': os.environ.get('JWT_SECRET_KEY', 'test-secret-key'),
    })

    yield app

    with app.app_context():
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute('DELETE FROM users WHERE username LIKE %s', ('testuser_%',))
            cur.execute('DELETE FROM students WHERE student_name LIKE %s', ('teststudent_%',))
            conn.commit()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_token(client):
    unique_user = f'testuser_{int(time())}'

    client.post('/auth/register', json={
        'username': unique_user,
        'password': 'testpass'
    })

    response = client.post('/auth/login', json={
        'username': unique_user,
        'password': 'testpass'
    })

    data = response.get_json()
    return data['token']