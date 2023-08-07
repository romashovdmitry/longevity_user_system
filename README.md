# Longevity user management system

DRF API service for user registration, authentication, and user data management.

## Quick Start

**1. Clone the repository**

```
git init
git clone https://github.com/romashovdmitry/longevity_user_system.git
```
**2. There is a file example.env. Open this file, pass your comfortable values to variables and change name to .env.**

*SUPER_USERNAME, SUPER_PASSWORD, SUPER_EMAIL* - Constants for [automatic](https://github.com/romashovdmitry/longevity_user_system/blob/8a7151c13ef9207a7ddf85da684e9c5e27ddb395/docker-compose.yml#L10) [creation](https://github.com/romashovdmitry/longevity_user_system/blob/8a7151c13ef9207a7ddf85da684e9c5e27ddb395/user/management/commands/create_super_user.py#L12-L26) of admin superuser

*PASSWORD_START, PASSWORD_FINISH, DEFAULT_ALGO_HASH, CUSTOM_HASH_ALGO* - Constants for [custom hashing password](https://github.com/romashovdmitry/longevity_user_system/blob/8a7151c13ef9207a7ddf85da684e9c5e27ddb395/user/hash.py#L14-L29)

*DB_NAME, DB_USER, DB_PASSWORD* - Constants for [database creation](https://github.com/romashovdmitry/longevity_user_system/blob/8a33f0f546667c2d7e5718156acef2992c8f7532/longevity/settings.py#L76-L85)

*SECRET_KEY* - standart secret_key for Django project

**3. Run docker-compose**

```
docker-compose up
```

**4. Enjoy!**

Open [Swagger page](http://127.0.0.1:8080/docs/) to utilize Swagger for interacting with the application. 

## Stack

- [ ] Docker, docker compose for containerization
- [ ] Framework: Django
- [ ] API: Django Rest Framework (DRF)
- [ ] Database: MySQL
- [ ] Swagger for describing implemented methods in OpenAPI format

## API Endpoints

***Allow Any Permission***
- /token/
    - GET: returns access and refresh token
- /token/refresh/
    - GET: returns new access token via refresh token

***Admin Only Permission***
- /api/users/
    - GET: get list of users
    - POST: create new user, registrate
- /api/users/{id}/
  - GET: get information about any user
  - PUT: update information about any user
  - DELETE: delete any user

***JWT Authentication Permission***
- /api/users/delete_me
  - POST: delete autheniticated user
- /api/users/get/
  - GET: get information about autheniticated user
- /api/update_me/
  - PUT: update information about autheniticated user

## Task Requirements

**1. Implement secure password hashing and storage**: custom [password hashing](https://github.com/romashovdmitry/longevity_user_system/blob/f0885b0a09ed4de35ba1483780e3dcb57412ec24/user/hash.py#L14-L29) using static and dynamic salts(by user.id).

**2. Appropriate validation and error handling techniques**: [custom validation class](https://github.com/romashovdmitry/longevity_user_system/blob/f0885b0a09ed4de35ba1483780e3dcb57412ec24/api/validation.py#L13-L138) with a lot of validation methods.

**3. Authentication and authorization mechanisms**: JWT authentication.

## Production

API is accessible at the following link: http://1507839-cy37741.tw1.ru:8080/docs/

For deployment, GitHub Actions are utilized for continuous [integration and continuous delivery (CI/CD)](https://github.com/romashovdmitry/longevity_user_system/blob/master/.github/workflows/longevity-deploy.yml). Minimal Nginx configurations have been set up on the server.

## It Would Be Good

1. To add logging
2. To add swagger_auto_schema for describing possible responses
3. Configure the server for SSL
