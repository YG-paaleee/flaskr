import time


class TestAuthAPI:

    def test_register_success(self, client):
        unique_user = f'testuser_{int(time.time())}'
        
        response = client.post('/auth/register', json={
            'username': unique_user,
            'password': 'testpass123'
        })
        
        assert response.status_code == 201
        data = response.get_json()
        assert data['status'] == 'success'
    
    def test_register_missing_fields(self, client):
        response = client.post('/auth/register', json={
            'username': 'testuser'
        })
        
        assert response.status_code == 400
    
    def test_register_duplicate_user(self, client):
        client.post('/auth/register', json={
            'username': 'duplicate_user',
            'password': 'pass123'
        })
        
        response = client.post('/auth/register', json={
            'username': 'duplicate_user',
            'password': 'pass123'
        })
        
        assert response.status_code == 400
    
    def test_login_success(self, client):
        client.post('/auth/register', json={
            'username': 'logintest',
            'password': 'testpass'
        })
        
        response = client.post('/auth/login', json={
            'username': 'logintest',
            'password': 'testpass'
        })
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'token' in data
    
    def test_login_wrong_password(self, client):
        response = client.post('/auth/login', json={
            'username': 'logintest',
            'password': 'wrongpassword'
        })
        
        assert response.status_code == 401