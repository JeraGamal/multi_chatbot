FastAPI Application

This project is a FastAPI-based application designed to handle user authentication, chatbots, and document processing functionalities.

Features
- **User Authentication**: Register and log in users with secure password hashing.
- **Chatbot Integration**: Handle chatbot-related requests (add, retrieve, and manage chatbots).
- **Document Processing**: Basic NLP operations using NLTK.

## Installation

1. Create a Virtual Environment


- python -m venv venv
- source venv/bin/activate  # For Linux/Mac
- venv\Scripts\activate     # For Windows
  
2. Install Dependencies

- pip install -r requirements.txt
- Set Up the Database Run the script to create tables in the database:
- python create_tables.py

  
3. Start the Server Run the FastAPI application with Uvicorn:


- uvicorn app.main:app --reload
- Access the Application

- API documentation: http://127.0.0.1:8000/docs
- Swagger UI: http://127.0.0.1:8000/redoc



4. Testing the API
Use the following tools to test API endpoints:

cURL:

curl -X POST "http://127.0.0.1:8000/auth/register" \
     -d "username=user&email=user@example.com&password=secret"
Postman or Swagger UI: Access http://127.0.0.1:8000/docs.


5. Dependencies
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Passlib
- NLTK
- SQLite (default database)
