# Django REST Framework Project

This project is a Django REST API that includes user registration, login, JWT authentication, and friend request management functionalities.

## Features

- User registration with email and password
- Token authentication for login and logout
- Search users by email and name
- Send, accept, and reject friend requests
- List friends and pending friend requests
- Rate limiting for sending friend requests

## Requirements

- Python 3.8+
- Django 4.2+
- Django REST Framework

## Setup

1. **Clone the repository**:

    git clone 
    cd social_network

2. **Create a virtual environment**:

    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`

3. **Install dependencies**:

    pip install -r requirements.txt

4. **Apply migrations**:

    python3 manage.py makemigrations
    python3 manage.py migrate

5. **Run the server**:

    python3 manage.py runserver

## Setup with Docker
1. **Clone the repository**:

    git clone 
    cd social_network

2. **Build and run the Docker containers**:
    docker-compose up --build

3. **Apply migrations**:
    docker-compose exec web python manage.py migrate

4. **Create a superuser**:
    docker-compose exec web python manage.py createsuperuser


## Endpoints

- **Register**: `POST /api/register/`
  
  ```json
  {
    "username": "test",
    "email": "test@gmail.com",
    "password": "Asdf@123",
    "confirm_password": "Asdf@123"
  }

  ```response
  {
    "id": 1,
    "username":"test",
    "email":"test@gmail.com"
  }


-  **Login**: `POST /api/login/`

  ```json
  {
    "email":"test@example.com",
    "password":"password123"
  }

  ```response
  {
    "token": "<token>",
    "user_id": 1,
    "email": "test@example.com"
  }


-  **Logout**:`POST /api/logout/`

  ```json
  {
    "token": "your-token"
  }

  ```response
  {
    "message": "Successfully logged out."
  }


-  **Search Users**: `GET /api/search/?search=<keyword>` 
  ```json
  {
    "token": "your-token"
  }

  ```response
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "keyword",
            "email": "keyword@gmail.com"
        },
        {
            "id": 2,
            "username": "keyword",
            "email": "keyword@gmail.com"
        },
    ]
  }

-  **Send Friend Request**: `POST /api/friend-requests/send/`

  ```json
  {
    "email_or_username": "email_or_username"
  }

  ```response
  {
    "id": 1,
    "from_user": {
        "id": 1,
        "username": "test",
        "email": "test@gmail.com"
    },
    "to_user": {
        "id": 2,
        "username": "test2",
        "email": "test2@example.com"
    },
    "timestamp": "2024-06-04T05:54:36.018593Z",
    "accepted": false
  }

-  **Accept Friend Request**: `PUT /api/friend-requests/accept/`

  ```json
  {
    "email_or_username": "email_or_username"
  }
  ```response
  {
    "message": "Friend request accepted",
    "friend_request": {
        "id": 1,
        "from_user": {
            "id": 1,
            "username": "test",
            "email": "test@gmail.com"
        },
        "to_user": {
            "id": 2,
            "username": "test2",
            "email": "test2@gmail.com"
        },
        "timestamp": "2024-06-04T11:36:46.834219Z",
        "accepted": true
    }
  }


-  **Reject Friend Request**: `DELETE /api/friend-requests/reject/`

  ```json
  {
    "email_or_username": "email_or_username"
  }

  ```response
  {
    "message": "Friend request rejected successfully."
  }


-  **List Friends**: `GET /api/friends/`
  ```json
  {
    "token": "your-token"
  }

  ```response
  [
    {
        "id": 1,
        "username": "test",
        "email": "test@gmail.com"
    }
    {
        "id":2,
        "username": "test3",
        "email": "test3@gmail.com"
    }
  ]


-  **List Pending Friend Requests**: `GET /api/friend-requests/pending/`
  ```json
  {
    "token": "your-token"
  }

  ```response
  [
    {
        "id": 1,
        "from_user": {
            "id": 1,
            "username": "test",
            "email": "test@gmail.com"
        },
        "timestamp": "2024-06-04T11:36:46.834219Z",
        "accepted": false
    }
  ]







