# Initial infrastructure for the project

## Frontend
    * React
    * react router for pagination

## Backend
    * Django

## DB
    * postgresql
    * data currently held locally. file was too large to push to github

## Containerized with Docker


To run backend/db for development  
    * Have Docker Desktop Running  
    * open terminal to "backend" directory  

    $ docker-compose up -d --build
    $ docker-compose exec web python manage.py migrate
    $ docker-compose down
    $ docker-compose up -d --build

    * It's a little sloppy right now. The final container setup isn't in place yet

To run frontend for development  
    * open terminal to "frontend" directory

    $ npm install
    $ npm run dev
