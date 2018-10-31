## Simple React-based web form, Flask API and PostgreSQL database with Docker-compose and nginx

## About
This application consists of:
* A basic web form built using React
* A Flask API 
* nginx reverse proxy
* Docker-compose

## Prerequisites
To run the full application you will need to:
1. Clone the repo
2. Install Docker and Docker Compose

## Running the application
At the project root, run:
1. `docker-compose -f docker-compose.yml up -d --build`
2. `docker-compose -f docker-compose.yml run form-handler python manage.py recreate-db`
3. `docker-compose -f docker-compose.yml run form-handler python manage.py seed-db`
4. `docker-compose up -d`

The application will be available at http://localhost/

API endpoints will be available at:
* http://localhost/api/food/categories
* http://localhost/api/food/types

Submissions, locations and new food types are not visible in the API, but you can see what’s happening in the database with:

`docker-compose -f docker-compose.yml exec db psql -U postgres`

To run the React form alone, you will need to:
1. `cd web_form`
2. Install the dependencies by running `npm install`
3. Start the server with `npm start`

## Running tests

To run tests for the Flask API:
1. `docker-compose -f docker-compose.yml run form-handler python manage.py test`

To run tests for the React form:
1. `cd web_form`
2. `npm test`

## Killing the application
Kill everything with `docker-compose down`