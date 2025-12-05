📚 Libro – Library Management System (FastAPI + PostgreSQL)

Libro is a simple yet scalable Library Management System built using FastAPI, PostgreSQL, and SQLAlchemy ORM.

It supports:
	•	Adding & managing books
	•	Registering users
	•	Borrowing books
	•	Returning books
	•	Tracking loan history
	•	Auto-generated API documentation

⸻

🚀 Project Purpose

This project demonstrates:
	•	FastAPI backend development
	•	PostgreSQL + SQLAlchemy integration
	•	Real-world transactional workflows for borrow/return
	•	API validation with Pydantic v2
	•	Clean architecture for maintainability

⸻

🏗️ Project Structure

main.py  
models.py  
schemas.py  
crud.py  
database.py  
requirements.txt  
tests/  
README.md


⸻

⚙️ Setup Instructions

1. Install PostgreSQL

Mac (Homebrew):

brew install postgresql
brew services start postgresql

Create database:

psql postgres
CREATE DATABASE libro_db;

2. Create Virtual Environment

python3 -m venv venv
source venv/bin/activate

3. Install Requirements

pip install -r requirements.txt

4. Create .env

DATABASE_URL=postgresql://<username>:<password>@localhost:5432/libro_db

Example:

DATABASE_URL=postgresql://nityashukla:password@localhost:5432/libro_db


⸻

▶️ Run the Application

Start FastAPI:

uvicorn main:app --reload

Open API docs:
	•	Swagger: http://127.0.0.1:8000/docs
	•	ReDoc: http://127.0.0.1:8000/redoc

⸻

🧪 Run Tests

pytest -v


⸻

📘 API Usage Examples

➤ Create a Book

curl -X POST "http://127.0.0.1:8000/books" \
-H "Content-Type: application/json" \
-d '{
  "title": "Book A",
  "author": "Author A",
  "isbn": "ISBN001",
  "publication_year": 2024,
  "total_copies": 3
}'

➤ Get All Books

curl http://127.0.0.1:8000/books

➤ Update Book

curl -X PUT "http://127.0.0.1:8000/books/1" \
-H "Content-Type: application/json" \
-d '{"title": "Updated Title"}'


⸻

👤 USER API

➤ Create User

curl -X POST "http://127.0.0.1:8000/users" \
-H "Content-Type: application/json" \
-d '{
  "name": "Nitya",
  "email": "nitya@example.com"
}'

➤ Get Users

curl http://127.0.0.1:8000/users


⸻

🔄 LOAN APIs

📖 Borrow Book

curl -X POST "http://127.0.0.1:8000/books/1/borrow" \
-H "Content-Type: application/json" \
-d '{"user_id": 1}'

🔁 Return Book

curl -X POST "http://127.0.0.1:8000/loans/1/return"

📄 Get Loans

curl http://127.0.0.1:8000/loans


⸻

🧹 Reset Database (Optional)

psql libro_db
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;


⸻

📝 Self-Reflection

I learned:
	•	Structuring a real-world FastAPI backend
	•	PostgreSQL + SQLAlchemy ORM usage
	•	Implementing borrow/return transactional logic
	•	Debugging validation and database errors
	•	Building a maintainable API layer
