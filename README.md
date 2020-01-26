# Lambda Arena User and Authentication Server
This server uses the django-rest-framework and django-rest-auth packages for user creation and authentication. 

## Data management
The backend is configured to work with postgres. 

### Development
In order to connect to your postgres database you will need the environmental variables
below in your `.env` file.
```
DEV_BD_PW=xxxxxxxxxxxx
DEV_DB_NAME=xxxxxxxxxx
DEV_DB_USER=xxxxxxxxx
DEV_DB_ENDPOINT=xxxxxxxxxxxxx
DEV_DB_PORT=xxxx
SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

To build your tables run the migrations with the command `python manage.py migrate`

### Production
This server is configured for deployment on Heroku. The `django-heroku` package 
manages the database connection. Once the database has been deployed the migration 
need to be run. You can use the Heroku CLI run the command `heroku run python manage.py migrate`


The API endpoints documentation below is courtesy of [django-rest-atuh documentation](https://github.com/Tivix/django-rest-auth)

API endpoints
=============

Basic
-----

- /rest-auth/login/ (POST)

    - username
    - email
    - password

    Returns Token key

- /rest-auth/logout/ (POST)

    .. note:: ``ACCOUNT_LOGOUT_ON_GET = True`` to allow logout using GET - this is the exact same configuration from allauth. NOT recommended, see: http://django-allauth.readthedocs.io/en/latest/views.html#logout

- /rest-auth/password/reset/ (POST)

    - email

- /rest-auth/password/reset/confirm/ (POST)

    - uid
    - token
    - new_password1
    - new_password2

    .. note:: uid and token are sent in email after calling /rest-auth/password/reset/

- /rest-auth/password/change/ (POST)

    - new_password1
    - new_password2
    - old_password

    .. note:: ``OLD_PASSWORD_FIELD_ENABLED = True`` to use old_password.
    .. note:: ``LOGOUT_ON_PASSWORD_CHANGE = False`` to keep the user logged in after password change

- /rest-auth/user/ (GET, PUT, PATCH)

    - username
    - first_name
    - last_name

    Returns pk, username, email, first_name, last_name


Registration
------------

- /rest-auth/registration/ (POST)

    - username
    - password1
    - password2
    - email

- /rest-auth/registration/verify-email/ (POST)

    - key


Social Media Authentication
---------------------------

Basing on example from installation section :doc:`Installation </installation>`

- /rest-auth/facebook/ (POST)

    - access_token
    - code

    .. note:: ``access_token`` OR ``code`` can be used as standalone arguments, see https://github.com/Tivix/django-rest-auth/blob/master/rest_auth/registration/views.py

- /rest-auth/twitter/ (POST)

    - access_token
    - token_secret