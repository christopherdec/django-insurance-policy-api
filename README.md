# Django Insurance Policy API

This repo contains the project of a basic API for the CRUD of insurance policies.

It was developed for a code assignment, using the Django REST Framework.

## Setup instructions

1. Open a terminal, clone the repo and navigate to its root directory.
2. Create a new virtual environment:
```
python -m venv venv
```
3. If you're on Linux/macOS, activate the virtual environment with:
```
source venv/bin/activate
```
If you're on Windows, execute:
```
venv\Scripts\activate
```
4. Install dependencies with:
```
pip install -r requirements.txt
```
5. Before starting the application, you should run the database migrations with:
```
python manage.py migrate
```
The database used by this project is sqlite3, which comes with Python.

## Executing the application

After you have configured the virtual environment and applied the migrations, you can start the dev server
with:
```
python manage.py runserver
```

Now you can access `localhost:8000` in your browser and explore the API!

## Suggested next steps

Here are some improvements that I would consider developing next, not necessarily in this order:

- Add Swagger and versioning
- Add pagination
- Add rate limiting
- Add authentication
- Add validation in the Serializers
- Add more complexity, e.g., a `Customer` table with a relationship with `Policy`
    