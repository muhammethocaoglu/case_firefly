#Customer Api

It is implemented using Django rest framework. Django was selected due to its environment enabling more rapid development with built-in ORM support. Embedded database SQLite3 was used in implementation.

##How to run:

In order to run it, following commands should be run in terminal: 

pipenv install djangorestframework

python manage.py migrate

python manage.py runserver

##REST endpoints:

Login (POST): Gets email and password fields in request body, and returns SUCCESS if there is a matching password for given e-mail.

Register (POST): Gets email, password, first_name, and last_name fields in request body, and returns CREATED.

List (GET): Lists all customers

Patch (PATCH): Updates some or all fields of a customer with id given in path excluding id and password

Delete (DELETE): Deletes customer with id given in path

Retrieve (GET): Retrieves customer with id given in path

##Running customer app in Docker:

Following commands should be run in terminal:

docker build -t customerapi .

docker run -d -p 8000:8000 customerapi

You can reach out your application from your web browser with the following url: localhost:8000






