# no-framework-client-server-web-form
Mini-project for work

This is a web-page with register form, logging in modifying user information made with python.
It's was built using http.server module for serving requests and jinja2 to render dynamic pages.

## Features
You can register with valid information, login to your account and change your first name, last name and password once logged in.

## Files
main.py is the file that you need to run to start the server, create the database if does not exist and listen for requests.
envs.py has important variables that did not have a plce in the main.py or had to be shared between files.
db_service_interface is an abstact interface class for working with the database.
db_service is implementation for the db_service_interface that is used in the controller.py to connect and work with the database.
controller is the link between the http server and the database that has the logic and restrictions for the inputs and outputs.

## Built-in functions used
http.server.BaseHTTPRequestHandler is used for handling GET and POST requests.
jinja2 and it's .template(...) and .render(...) are used to display dynamic pages.