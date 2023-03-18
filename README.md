# Student-API

## Aim
Using [Python](https://www.python.org/), [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/), [PostgreSQL](https://www.postgresql.org), and [Swagger UI](https://swagger.io/tools/swagger-ui/) to build a student management API.

## Summary
This project is an API for managing students and courses. It includes endpoints for creating, reading, updating, and deleting students and courses. 
Students have a name, ID, and email address. Courses have a name, ID, teacher and list of registered students. 
The API also includes functionality for registering courses and retrieving grades. GPA is calculated using the standard 4.0 scale.
The API is secured with JWT tokens for authentication and authorization. It is worth noting that admins have access to all routes and resources, and all routes are admin protected, and only an authenticated admin can create another admin. But for the purposes of testing, the route for creating an admin will be open.

This API was built as a Third Semester exam project by [Alexander](https://github.com/Anyaegbunam-Alexander), a Backend Engineering student of [AltSchool Africa](https://www.altschoolafrica.com/).

## Built With
- [Python](https://www.python.org/)
- [Flask-RESTX](https://flask-restx.readthedocs.io/en/latest/)
- [Flask-JWT](https://flask-jwt-extended.readthedocs.io/en/stable/)
- [PostgreSQL](https://www.postgresql.org)

## Installation
Install with pip:
```
pip install -r requirements.txt
```

## Setup and Configuration

### `.env` Configuration
Create a .env file with these configurations:
```

FLASK_DEBUG=<True/False>
FLASK_APP=app.py
SECRET_KEY=<your secret key>
DATABASE_URL = <database URL>
JWT_SECRET_KEY = <JWT secrete key>
ALGORITHM = <hashing algorithm>
ACCESS_TOKEN_EXPIRES_MINUTES = <expiration time of the access and refresh tokens>

```  
Note: The `DATABASE_URL` setting is not required but it must have a value even if an arbitrary value for your app to run during development and testing. But during production, this must be set to a valid database URL.  


## App Setup

In the file `app.py` which is in the base directory, in line 4, the argument for the `create_app` function is currently set to `config_dict['production']`. 
You can remove the argument entirely as the default argument value is set to `config_dict['dev']` in the `__init__.py` file in the `api` folder, which is the configuration for development.
You can find different configurations in the `config.py` file which is in the `config` folder.



## Run Flask
In the terminal:
```
 flask run
```
In Flask, the default port is 5000  

Entry point: `http://localhost:5000/`


## Contact
- Mail: alexanderking.aa@gmail.com
- GitHub: [Alexander](https://github.com/Anyaegbunam-Alexander)

## Acknowledgements
- [AltSchool Africa](https://www.altschoolafrica.com/)
- [Caleb Emelike](https://github.com/CalebEmelike)
- [Stack Overflow](https://stackoverflow.com/)
