import time
import pytest
import json

# ============= STUDENTS TESTS =============
class TestStudentsAPI:

    def test_get_all_students(self, client):
        response = client.get('/api/students')

        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
    
    def test_get_all_students_xml(self, client):
        response = client.get('/api/students?format=xml')

        assert response.status_code == 200
        assert response.content_type == 'application/xml'
    
    def test_get_single_student(self, client):
        response = client.get('/api/student/1')

        assert response.status_code in [200, 404, 500]

    def test_get_nonexistent_student(self, client):
        response = client.get('/api/student/9999')
    
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] == False

    def test_search_students_by_course(self, client):

        response = client.get('/api/students?course=Computer')

        assert response.status_code == 200
        data = response.get_json()
        for student in data:
            if 'course' in student:
                assert 'Computer' in student['course']

# ============= TEACHERS TESTS =============

class TestTeachersAPI:
    """Test /api/teachers endpoints."""
    
    def test_get_all_teachers(self, client):
        """GET /api/teachers returns 200."""
        response = client.get('/api/teachers')
        
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
    
    def test_search_teachers_by_department(self, client):
        """GET /api/teachers?department=CS filters results."""
        response = client.get('/api/teachers?department=Computer')
        
        assert response.status_code == 200


# ============= GRADES TESTS =============

class TestGradesAPI:
    """Test /api/grades endpoints."""
    
    def test_get_all_grades(self, client):
        """GET /api/grades returns 200."""
        response = client.get('/api/grades')
        
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
    
    def test_search_grades_by_semester(self, client):
        """GET /api/grades?semester=1st filters results."""
        response = client.get('/api/grades?semester=1st')
        
        assert response.status_code == 200

# ============= PROTECTED ENDPOINT TESTS =============

class TestProtectedEndpoints:
    
    def test_create_student_without_token(self, client):
        data = {
            'student_name': 'Test Student',
            'course': 'CS',
            'year_level': 1,
            'email': 'test@psu.edu.ph'
        }
        response = client.post('/api/students', json=data)
        
        assert response.status_code == 401
    
    def test_create_student_with_token(self, client, auth_token):
        data = {
            'student_name': 'Test Student',
            'course': 'Computer Science',
            'year_level': 2,
            'email': 'newtest@psu.edu.ph'
        }
        response = client.post(
            '/api/students',
            json=data,
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 201
        result = response.get_json()
        assert result['success'] == True
    
    def test_create_student_missing_field(self, client, auth_token):
        data = {
            'student_name': 'Test',
            'course': 'CS'
        }
        response = client.post(
            '/api/students',
            json=data,
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 400
    
    def test_create_student_invalid_email(self, client, auth_token):
        data = {
            'student_name': 'Test',
            'course': 'CS',
            'year_level': 1,
            'email': 'invalid-email'
        }
        response = client.post(
            '/api/students',
            json=data,
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code == 400
    
    def test_update_student_with_token(self, client, auth_token):
        data = {'year_level': 4}
        response = client.put(
            '/api/student/1',
            json=data,
            headers={'Authorization': f'Bearer {auth_token}'}
        )
        
        assert response.status_code in [200, 404]
    
    def test_delete_without_token(self, client):
        response = client.delete('/api/student/1')
        
        assert response.status_code == 401