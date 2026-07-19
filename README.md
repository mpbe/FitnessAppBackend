# FitnessApp

A REST API built with FastAPI that providdes secure user authentication and workout management for the FitnessApp frontend.

## Deployment

- Backend deployed on Vercel https://fitness-app-green-eta.vercel.app/
- PostgreSQL database hosted on Neon

## Features

- User Registration
- JWT authentication
- Login system
- Protected endpoints
- Create, read, update, delete workouts
- Workouts specific to each user
- Pagination
- SQLAlchemy
- PostgreSQL Database
- CORS support for React Frontend
- Automated testing with pytest


## API Preview

![Swagger UI](./screenshots/api_preview.png)


## Tech Stack

- Python
- FastApi
- SQLAlchemy
- PostgreSQL
- JWT Authentication
- Passlib / bcrypt
- Pytest
- Uvicorn


## Installation

1. Clone the Repository:
git clone https://github.com/mpbe/FitnessApp.git

2. Create the virtual environment:
python -m venv venv

3. Activate environment:
venv\scripts\activate

4. Install dependencies:
pip install -r requirements.txt

5. Create .env and copy the contents of '.env.example' into it

6. Run server:
uvicorn app.main:app -reload

To test out the app, when the server is running navigate to:
http://127.0.0.1:8000/docs

## Future Improvements

- Docker deployment
- Refresh tokens for JWT authentication
- Rate limiting
- Improved API documentation

