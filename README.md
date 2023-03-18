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



## Requests
### Students
####  Create new student(s).
You can create just one student or more than one student. You just need to send a list of dictionaries with each student's details. Below is how the request would look like.
```
{"students" : [
                {
                    "name" : "John Doe 1",
                    "email" : "johndoe1@email.com",
                    "password" : "password1"
                },
                {
                    "name" : "John Doe 2",
                    "email" : "johndoe2email@email.com",
                    "password" : "password2"
                }
]}


```

#### Updating a student by id.
You can update the student's information including register them for courses. Below is how the request would look like.
```
{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "courses": [
        {
            "id": 4,
            "score": 0
        },
        {
            "id": 2,
            "score": 65.0
        },
        {
            "id": 3,
            "score": 0
        }
    ]
}

```
The ids are the course_ids.

#### Removing/Unregistering courses a student is enrolled in.
This endpoint is specifically from removing courses the student is enrolled in. Any id in this list will be removed from the student's courses if the course with that id exits. Below is how the request would look like.
```
{
    "courses": [3, 1]
}
```

### Teachers
#### Create new teacher(s)
You can create just one teacher or more than one teacher. You just need to send a list of dictionaries with each teacher's details.  
You **MUST** create teachers before creating courses.  
Below is how the request would look like.
```
{"teachers" : [
                {
                    "name" : "Teacher 1",
                    "email" : "teacher1@email.com"
                },
                {
                    "name" : "Teacher 2",
                    "email" : "teacher2@email.com"
                }
]}

```
#### Update a teacher by id  
Here you can only update the teacher's details but not the courses the teacher is taking. Below is how the request would look like.
```
{
	"name": "Teacher 1 (Updated)",
	"email": "teacher@email.com"
}
```

### Courses
#### Create new course(s)
You can also create one or multiple courses. You just need to send a list of dictionaries with each course's details. This is where you will assign the teacher to take the course by their id.  
Every course **MUST** have a teacher_id and the teacher_id **MUST** exist in the database.  
Below is how the request would look like.
```
{"courses" : [
                {
                    "title" : "Course 1",
                    "teacher_id" : "2",
                    "units" : 3
                },
                {
                    "title" : "Course 2",
                    "teacher_id" : "1",
                    "units" : 2
                }        
]}

```
### Update a course by id
Here you can update the units and the teacher taking the course. Below is how the request would look like.
```
{
 "title" : "Course 1",
 "teacher_id" : 4,
 "units" : 3
}
```

## Testing
There are a total of 13 tests. In the terminal, run `pytest` or `pytest -v`.

## Contact
- Mail: alexanderking.aa@gmail.com
- GitHub: [Alexander](https://github.com/Anyaegbunam-Alexander)

## Acknowledgements
- [AltSchool Africa](https://www.altschoolafrica.com/)
- [Caleb Emelike](https://github.com/CalebEmelike)
- [Stack Overflow](https://stackoverflow.com/)
