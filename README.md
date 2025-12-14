# PSU Student Management REST API

A Flask-based CRUD REST API with MySQL database, JWT authentication, and XML/JSON output support.

## 📋 Project Details

- **Database:** MySQL (`psu` schema)
- **Framework:** Flask 3.1.0
- **Authentication:** JWT (JSON Web Tokens)
- **Output Formats:** JSON (default), XML

---

## 🗂️ Database Schema

### Tables:
- **students** - Student records (id, student_name, course, year_level, email)
- **teachers** - Teacher records (id, teacher_name, department, email)
- **grades** - Grade records (id, student_id, subject, grade, semester)
- **users** - Authentication users (id, username, password)

### ERD:
See `projectsite/badangDB.sql` for complete schema.

---

## ⚙️ Installation

### Prerequisites:
- Python 3.10+
- MySQL Server
- Git

### Steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YG-paaleee//flaskr.git
   cd flaskr
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r projectsite/requirements.txt
   ```

4. **Setup database:**
   ```bash
   mysql -u root -p < projectsite/badangDB.sql
   ```

5. **Configure environment variables:**
   
   Create `.env` file in project root:
   ```env
   SECRET_KEY=your-secret-key
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=your-mysql-password
   MYSQL_DB=psu
   JWT_SECRET_KEY=your-jwt-secret-key
   ```

6. **Run the application:**
   ```bash
   flask --app projectsite run --debug
   ```

7. **Access the API:**
   - Web Interface: `http://127.0.0.1:5000`
   - API Endpoints: `http://127.0.0.1:5000/api/`

---

## 🔐 Authentication

### Register a new user:
```http
POST /auth/register
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

### Login to get JWT token:
```http
POST /auth/login
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "status": "Success",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "username": "your_username"
}
```

### Using the token:
Include the token in the `Authorization` header for protected endpoints:
```
Authorization: Bearer <your_token>
```

---

## 📡 API Endpoints

### Students

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/students` | Get all students | ❌ |
| GET | `/api/student/<id>` | Get student by ID | ❌ |
| POST | `/api/students` | Create new student | ✅ |
| PUT | `/api/student/<id>` | Update student | ✅ |
| DELETE | `/api/student/<id>` | Delete student | ✅ |

### Teachers

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/teachers` | Get all teachers | ❌ |
| GET | `/api/teacher/<id>` | Get teacher by ID | ❌ |
| POST | `/api/teachers` | Create new teacher | ✅ |
| PUT | `/api/teacher/<id>` | Update teacher | ✅ |
| DELETE | `/api/teacher/<id>` | Delete teacher | ✅ |

### Grades

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/grades` | Get all grades | ❌ |
| GET | `/api/grade/<id>` | Get grade by ID | ❌ |
| POST | `/api/grades` | Create new grade | ✅ |
| PUT | `/api/grade/<id>` | Update grade | ✅ |
| DELETE | `/api/grade/<id>` | Delete grade | ✅ |

---

## 📤 Output Formats

### JSON (default):
```http
GET /api/students
```

### XML:
```http
GET /api/students?format=xml
```

---

## 🔍 Search & Filter

### Search students by course:
```http
GET /api/students?course=Computer
```

### Search students by name:
```http
GET /api/students?name=Juan
```

### Search teachers by department:
```http
GET /api/teachers?department=Science
```

### Search grades by semester:
```http
GET /api/grades?semester=1st
```

---

## 📝 Usage Examples

### Create a student (with JWT):
```bash
curl -X POST http://127.0.0.1:5000/api/students \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token>" \
  -d '{
    "student_name": "Datu Samir Vitug",
    "course": "Computer Science",
    "year_level": 3,
    "email": "messikaramessi_rm@psu.edu.ph"
  }'
```

### Get all students as XML:
```bash
curl http://127.0.0.1:5000/api/students?format=xml
```

### Update a student:
```bash
curl -X PUT http://127.0.0.1:5000/api/student/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token>" \
  -d '{
    "year_level": 4
  }'
```

### Delete a student:
```bash
curl -X DELETE http://127.0.0.1:5000/api/student/1 \
  -H "Authorization: Bearer <your_token>"
```

---

## 🧪 Running Tests

```bash
pytest projectsite/tests/ -v
```

### Test Coverage:
- ✅ Students CRUD operations
- ✅ Teachers CRUD operations
- ✅ Grades CRUD operations
- ✅ Authentication (register/login)
- ✅ Input validation
- ✅ Protected endpoints
- ✅ XML/JSON output formats

---

## 📁 Project Structure

```
flaskr/
├── projectsite/
│   ├── __init__.py        # App factory
│   ├── api.py             # REST API endpoints
│   ├── auth.py            # JWT authentication
│   ├── db.py              # Database connection
│   ├── views.py           # Web views
│   ├── badangDB.sql       # Database schema
│   ├── requirements.txt   # Dependencies
│   ├── static/            # CSS files
│   ├── templates/         # HTML templates
│   └── tests/             # Unit tests
│       ├── conftest.py    # Test fixtures
│       ├── test_api.py    # API tests
│       └── test_auth.py   # Auth tests
├── .env                   # Environment variables (not in repo)
├── .gitignore
└── README.md
```

---

## 🛠️ Technologies Used

- **Flask** - Web framework
- **Flask-MySQLdb** - MySQL database connector
- **Flask-JWT-Extended** - JWT authentication
- **python-dotenv** - Environment variable management
- **pytest** - Testing framework
- **Werkzeug** - Password hashing

---

## 👤 Author

**Ralph Angelo Badang**

---