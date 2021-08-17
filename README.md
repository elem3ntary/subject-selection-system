# Subject selection system
[![Requirements Status](https://requires.io/github/elem3ntary/subject-selection-system/requirements.svg?branch=master)](https://requires.io/github/elem3ntary/subject-selection-system/requirements/?branch=master)

RESTful API build with ❤️ and FastAPI.


## Description
System that simplify the process of choosing subjects in selective disciplines. Also allows admins to create, modify and delete subjects.

## Endpoints
```
POST /login
POST /register

GET  /user/subjects -> returns available subjects
POST /user/subjects/choose -> choose subjects

POST /admin/subject/create
PUT /admin/subject/{subject_id}
DELETE /admin/subject/{subject_id}
PATCH /admin/config -> edit registration status


```
## Instalation
```bash
$ pip3 install requirements.txt
```

## Usage
```bash
$ uvicorn app.main:app --port 3000
```

## Technologies
+ FastAPI
+ SQLAlchemy
+ Pydantic
+ JWT


## License
MIT