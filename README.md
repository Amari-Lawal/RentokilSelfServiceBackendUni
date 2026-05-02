# Rentokil Self-Service Backend

A robust FastAPI backend for managing insect extermination appointments.

## Features
- **JWT Authentication**: Secure user registration and login.
- **Role-Based Access**: Admin and Customer roles.
- **Database**: SQLite with SQLAlchemy ORM.
- **Health Checks**: Built-in health endpoint for monitoring.
- **Custom Exceptions**: Descriptive error handling for configuration and runtime issues.

## Environment Setup
Create a `.env` file in this directory with the following variables:
```env
DATABASE_URL=sqlite:///./app.db
JWT_SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
*Note: A default key is provided when running via the `RentokilLocalStackUni` for local development.*

## Running Locally (Standalone)
If you wish to run the backend outside of Docker:
1. Create a virtual environment: `python -m venv venv`
2. Activate it: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the app: `uvicorn main:app --reload --port 8080`

## Testing
To run unit tests:
```bash
pytest
```
Or via the local stack build script:
```bash
../RentokilLocalStackUni/build_app.sh --test
```

## API Documentation
Once running, visit:
- **Swagger UI**: [http://localhost:8080/docs](http://localhost:8080/docs)
- **ReDoc**: [http://localhost:8080/redoc](http://localhost:8080/redoc)
