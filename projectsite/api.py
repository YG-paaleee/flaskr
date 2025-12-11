from .db import get_db
from flask import Blueprint,jsonify, request, make_response
import dicttoxml

apiBp = Blueprint('api', __name__, url_prefix = '/api')

#helper functions

def format_response(data, status_code=200):
    format_type = request.args.get('format', 'json').lower()

    if format_type == 'xml':
        xml = dicttoxml.dicttoxml(data, custom_root='response', attr_type=False)
        response = make_response(xml, status_code)
        response.headers['Content-Type'] = 'application/xml'
        return response
    else:
        return jsonify(data), status_code

# ------------- API ENDPOINTS ---------------
# students endpoint

@apiBp.route('/students', methods=['GET'])
def get_students_data():
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM students')
            students = cur.fetchall()

        return format_response(students)
    
    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }
        , 500)

@apiBp.route('/student/<int:student_id>', methods=['GET'])
def get_student_api(student_id):

    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM students WHERE id = %s', (student_id,))
            student = cur.fetchone()
        
        if not student:
            return format_response(
                {
                    'success': False,
                    'error': 'student not found'
                }
            , 404)
        
        return format_response(student)
    
    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }
        , 500)

@apiBp.route('/students', methods=['POST'])
def create_students():

    try:
        data = request.get_json()
        required_fields = ['student_name', 'course', 'year_level', 'email']
        conn = get_db()


        for field in required_fields:
            if field not in data or not data[field]:
                return format_response(
                    {
                        'success': False,
                        'error': f'missing required field: {field}'
                    }
                ), 400
            
        if '@' not in data['email']:
            return format_response(
                {
                    'success': False,
                    'error': 'invalid email formats'
                }
            ), 400
        
        with conn.cursor() as cur:
            cur.execute('INSERT INTO students (student_name, course, year_level, email) VALUES (%s, %s, %s, %s)',
            (data['student_name'], data['course'], data['year_level'], data['email']))

            conn.commit()
            new_id = cur.lastrowid

        return format_response(
            {
                'success': True,
                'message': f'student {new_id} created successfully'
            }, 201)

    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }    
        , 500)

@apiBp.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    try:

        data = request.get_json()

        ALLOWED_FIELDS = ("student_name", "course", "year_level", "email")
        update_fields, params = [], []

        conn = get_db()

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
            student = cur.fetchone()

            if not student:
                return format_response(
                    {
                        'success': False,
                        'error': 'student not found'
                    }
                , 404)

            for field in ALLOWED_FIELDS:
                if field in data:
                    if field == 'email' and '@' not in data[field]:
                        return format_response({
                            'success': False,
                            'error': 'Invalid email format'
                        }), 400
                    
                    update_fields.append(f"{field} = %s")
                    params.append(data[field])
            
            if not update_fields:
                return format_response({
                    'success': False,
                    'error': 'No fields to update'
                }, 400)

            params.append(student_id)
            cur.execute(f"UPDATE students SET {', '.join(update_fields)} WHERE id = %s", params)
            conn.commit()

        return format_response(
            {
                'success': True,
                'message': f'student {student_id} updated successfully'
            }
        )
            
    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }
        , 500)
    
@apiBp.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        conn = get_db()

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
            student = cur.fetchone()

            if not student:
                return format_response(
                    {
                        'success': False,
                        'error': f'student {student_id} doesn\'t exist'
                    }
                , 404)
            
            cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
            conn.commit()

        return format_response(
            {
                'success': True,
                'message': f'student {student_id} deleted successfully'
            }
        )

    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }
        , 500)

# teachers endpoints

@apiBp.route('/teachers', methods=['GET'])
def get_teachers_data():
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM teachers')
            teachers = cur.fetchall()

        return format_response(teachers)
    
    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }, 500)
    
@apiBp.route('/teacher/<int:teacher_id>', methods=['GET'])
def get_teacher_api(teacher_id):
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM teachers WHERE id = %s', (teacher_id,))
            teacher = cur.fetchone()
        
        if not teacher:
            return format_response(
                {
                    'success': False,
                    'error': 'teacher not found'
                }
            , 404)
        
        return format_response(teacher)
    
    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }, 500)

@apiBp.route('/teachers', methods=['POST'])
def create_teachers():
    try:
        data = request.get_json()
        required_fields = ['teacher_name', 'department', 'email']
        conn = get_db()


        for field in required_fields:
            if field not in data or not data[field]:
                return format_response(
                    {
                        'success': False,
                        'error': f'missing required field: {field}'
                    }, 400)
            
        if '@' not in data['email']:
            return format_response(
                {
                    'success': False,
                    'error': 'invalid email formats'
                }, 400)
        
        with conn.cursor() as cur:
            cur.execute('INSERT INTO teachers (teacher_name, department, email) VALUES (%s, %s, %s)',
            (data['teacher_name'], data['department'], data['email']))

            conn.commit()
            new_id = cur.lastrowid

        return format_response(
            {
                'success': True,
                'message': f'teacher {new_id} created successfully'
            }, 201)

    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }, 500)

@apiBp.route('/teacher/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    try:

        data = request.get_json()

        ALLOWED_FIELDS = ("teacher_name", "department", "email")
        update_fields, params = [], []

        conn = get_db()

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
            teacher = cur.fetchone()

            if not teacher:
                return format_response(
                    {
                        'success': False,
                        'error': 'teacher not found'
                    }
                , 404)

            for field in ALLOWED_FIELDS:
                if field in data:
                    if field == 'email' and '@' not in data[field]:
                        return format_response({
                            'success': False,
                            'error': 'Invalid email format'
                        }, 400)
                    
                    update_fields.append(f"{field} = %s")
                    params.append(data[field])
            
            if not update_fields:
                return format_response({
                    'success': False,
                    'error': 'No fields to update'
                }, 400)

            params.append(teacher_id)
            cur.execute(f"UPDATE teachers SET {', '.join(update_fields)} WHERE id = %s", params)
            conn.commit()

        return format_response(
            {
                'success': True,
                'message': f'teacher {teacher_id} updated successfully'
            }
        )
            
    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }, 500)

@apiBp.route('/teacher/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    try:
        conn = get_db()

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM teachers WHERE id = %s", (teacher_id,))
            teacher = cur.fetchone()

            if not teacher:
                return format_response(
                    {
                        'success': False,
                        'error': f'teacher {teacher_id} doesn\'t exist'
                    }
                , 404)
            
            cur.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
            conn.commit()

        return format_response(
            {
                'success': True,
                'message': f'teacher {teacher_id} deleted successfully'
            }
        )

    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }, 500)

# grades endpoints

@apiBp.route('/grades', methods=['GET'])
def get_grades_data():
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM grades')
            grades = cur.fetchall()

        return format_response(grades)
    
    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }, 500)

@apiBp.route('/grade/<int:grade_id>', methods=['GET'])
def get_grade_api(grade_id):
    try:
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute('SELECT * FROM grades WHERE id = %s', (grade_id,))
            grade = cur.fetchone()
        
        if not grade:
            return format_response(
                {
                    'success': False,
                    'error': 'grade not found'
                }
            , 404)
        
        return format_response(grade)
    
    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }, 500)

@apiBp.route('/grades', methods=['POST'])
def create_grades():
    try:
        data = request.get_json()
        required_fields = ['student_id', 'student_name', 'course_code', 'course_name', 'grade', 'semester', 'school_year']
        conn = get_db()


        for field in required_fields:
            if field not in data or not data[field]:
                return format_response(
                    {
                        'success': False,
                        'error': f'missing required field: {field}'
                    }, 400)
        
        with conn.cursor() as cur:
            cur.execute('INSERT INTO grades (student_id, student_name, course_code, course_name, grade, semester, school_year) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (data['student_id'], data['student_name'], data['course_code'], data['course_name'], data['grade'], data['semester'], data['school_year']))

            conn.commit()
            new_id = cur.lastrowid

        return format_response(
            {
                'success': True,
                'message': f'grade {new_id} created successfully'
            }, 201)

    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }, 500)

@apiBp.route('/grade/<int:grade_id>', methods=['PUT'])
def update_grade(grade_id):
    try:

        data = request.get_json()

        ALLOWED_FIELDS = ("student_name", "course_code", "course_name", "grade", "semester", "school_year")
        update_fields, params = [], []

        conn = get_db()

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM grades WHERE id = %s", (grade_id,))
            grade = cur.fetchone()

            if not grade:
                return format_response(
                    {
                        'success': False,
                        'error': 'grade not found'
                    }
                , 404)

            for field in ALLOWED_FIELDS:
                if field in data:
                    update_fields.append(f"{field} = %s")
                    params.append(data[field])
            
            if not update_fields:
                return format_response({
                    'success': False,
                    'error': 'No fields to update'
                }, 400)

            params.append(grade_id)
            cur.execute(f"UPDATE grades SET {', '.join(update_fields)} WHERE id = %s", params)
            conn.commit()

        return format_response(
            {
                'success': True,
                'message': f'grade {grade_id} updated successfully'
            }
        )
            
    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }, 500)

@apiBp.route('/grade/<int:grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    try:
        conn = get_db()

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM grades WHERE id = %s", (grade_id,))
            grade = cur.fetchone()

            if not grade:
                return format_response(
                    {
                        'success': False,
                        'error': f'grade {grade_id} doesn\'t exist'
                    }
                , 404)
            
            cur.execute("DELETE FROM grades WHERE id = %s", (grade_id,))
            conn.commit()

        return format_response(
            {
                'success': True,
                'message': f'grade {grade_id} deleted successfully'
            }
        )

    except Exception as e:
        return format_response(
            {
                'success': False,
                'error': str(e)
            }, 500)