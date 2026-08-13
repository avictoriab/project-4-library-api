# Library Authentication API

A RESTful API built with Flask for managing a library of books with user authentication, JWT-based authorization, and user-owned resources.

## Features

* User registration with password hashing
* User login with JWT authentication
* Protected routes using a reusable authentication decorator
* Token expiration and validation
* Authorization based on book ownership
* Full CRUD operations for books
* User-specific book collection endpoint
* Input validation with Pydantic
* SQLAlchemy ORM with SQLite
* Consistent HTTP status codes and error responses
* Tested with Postman

## Technologies

* Python
* Flask
* SQLAlchemy
* Pydantic
* PyJWT
* SQLite
* python-dotenv
* Postman

## Project Structure

```text
library-api/
│
├── app.py
├── config.py
├── database.py
├── models.py
├── schemas.py
├── create_db.py
├── requirements.txt
├── .gitignore
├── .env
│
└── routes/
    ├── auth.py
    └── books.py
```

## Authentication

The API uses JSON Web Tokens (JWT) for authentication.

After successfully logging in, the API returns a token that must be included in the `Authorization` header when accessing protected endpoints:

```text
Authorization: Bearer <token>
```

Tokens expire after one hour.

The JWT secret key is stored in an environment variable and is never committed to the repository.

## Authorization

Authentication and authorization are handled separately.

* Authentication identifies the user through the JWT.
* Authorization verifies whether the authenticated user has permission to modify or delete a specific book.

A user can only update or delete books that belong to them.

## API Endpoints

### Authentication

| Method | Endpoint    | Authentication | Description                           |
| ------ | ----------- | -------------- | ------------------------------------- |
| POST   | `/register` | No             | Register a new user                   |
| POST   | `/login`    | No             | Authenticate a user and receive a JWT |

### Books

| Method | Endpoint      | Authentication | Description                                        |
| ------ | ------------- | -------------- | -------------------------------------------------- |
| GET    | `/books`      | No             | Retrieve all books                                 |
| POST   | `/books`      | Yes            | Create a new book                                  |
| GET    | `/books/<id>` | No             | Retrieve a specific book                           |
| PUT    | `/books/<id>` | Yes            | Update a book owned by the authenticated user      |
| DELETE | `/books/<id>` | Yes            | Delete a book owned by the authenticated user      |
| GET    | `/my-books`   | Yes            | Retrieve books belonging to the authenticated user |

## Example Requests

### Register

```http
POST /register
Content-Type: application/json
```

```json
{
  "username": "alice",
  "password": "password123"
}
```

### Login

```http
POST /login
Content-Type: application/json
```

```json
{
  "username": "alice",
  "password": "password123"
}
```

Response:

```json
{
  "token": "<jwt-token>"
}
```

### Create a Book

```http
POST /books
Authorization: Bearer <jwt-token>
Content-Type: application/json
```

```json
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald"
}
```

The authenticated user's ID is assigned automatically to the new book.

### Get User's Books

```http
GET /my-books
Authorization: Bearer <jwt-token>
```

Example response:

```json
{
  "books": [
    {
      "id": 1,
      "title": "The Great Gatsby",
      "author": "F. Scott Fitzgerald",
      "user_id": 1
    }
  ]
}
```

## Error Handling

The API uses standard HTTP status codes to communicate the result of requests.

| Status Code | Meaning                                     |
| ----------- | ------------------------------------------- |
| 200         | Request successful                          |
| 201         | Resource created successfully               |
| 400         | Invalid request or validation error         |
| 401         | Authentication required or invalid          |
| 403         | Authenticated user does not have permission |
| 404         | Resource not found                          |
| 409         | Resource conflict                           |

## Database

The project uses SQLite with SQLAlchemy as the ORM.

The database contains two main models:

```text
User
  │
  └───< Book
```

Each book belongs to one user through the `user_id` foreign key.

## Environment Variables

Create a `.env` file in the project root:

```env
JWT_SECRET_KEY=your-generated-secret-key
```

The `.env` file is excluded from version control through `.gitignore`.

## Setup

Clone the repository and create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

On Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create the database:

```bash
python create_db.py
```

Start the Flask development server:

```bash
python app.py
```

The API will be available at:

```text
http://127.0.0.1:5000
```

## Testing

The API was tested using Postman, including:

* Successful registration and login
* Invalid credentials
* JWT validation
* Expired tokens
* Missing and malformed authorization headers
* CRUD operations
* Input validation
* Resource ownership
* Unauthorized update and delete attempts
* User-specific book retrieval

## What I Learned

This project focused on building a backend API with authentication and authorization.

Key concepts practiced:

* Flask Blueprints
* REST API design
* SQLAlchemy relationships
* Password hashing
* JWT authentication
* Authentication vs. authorization
* Decorators
* Request validation with Pydantic
* Environment variables
* Database session management
* Resource ownership and access control
* HTTP status codes and API error handling
