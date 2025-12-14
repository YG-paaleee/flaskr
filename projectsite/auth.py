from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from projectsite.db import get_db

authBp = Blueprint('auth', __name__, url_prefix='/auth' )

@authBp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({
                'status': 'fail',
                'message': 'Username and password are required.'
            }), 400
        
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM users WHERE username = %s', (username,))
            if cur.fetchone():
                return jsonify({
                    'status': 'fail',
                    'message': 'User already exists.'
                }), 400
        
        hashed_password = generate_password_hash(password)

        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO users (username, password) VALUES (%s, %s)',
                (username, hashed_password)
            )
            conn.commit()

        return jsonify({
            'status': 'success',
            'message': 'User registered successfully.'
        }), 201


    except Exception as e:
        return jsonify(
            {
                'status': 'error',
                'message': str(e)
            }
        ), 500

@authBp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({
                'status': 'fail',
                'message': 'Username and password are required.'
            }), 400
        
        conn = get_db()
        with conn.cursor() as cur:
            cur.execute('SELECT id, password FROM users WHERE username = %s', (username,))
            user = cur.fetchone()
            if not user or not check_password_hash(user['password'], password):
                return jsonify({
                    'status': 'fail',
                    'message': 'Invalid username or password.'
                }), 401
            
            access_token = create_access_token(identity=str(user['id']))

        return jsonify({
            'status': 'Success',
            'token': access_token,
            'username': username
        }), 200

    except Exception as e:
        return jsonify(
            {
                'status': 'error',
                'message': str(e)
            }
        ), 500