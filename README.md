# Longevity user management system

DRF API service for user registration, authentication, and user data management.

## Quick Start

1. Clone the repository

```
git init
git clone https://github.com/romashovdmitry/longevity_user_system.git
```
2. There is a file example.env. Open this file, pass your comfortable values to variables and change name to .env. 

*SUPER_USERNAME, SUPER_PASSWORD, SUPER_EMAIL* - Constants for [automatic](https://github.com/romashovdmitry/longevity_user_system/blob/8a7151c13ef9207a7ddf85da684e9c5e27ddb395/docker-compose.yml#L10) [creation](https://github.com/romashovdmitry/longevity_user_system/blob/8a7151c13ef9207a7ddf85da684e9c5e27ddb395/user/management/commands/create_super_user.py#L12-L26) of admin superuser

*PASSWORD_START, PASSWORD_FINISH, DEFAULT_ALGO_HASH, CUSTOM_HASH_ALGO* - Constants for [custom hashing passwor](https://github.com/romashovdmitry/longevity_user_system/blob/8a7151c13ef9207a7ddf85da684e9c5e27ddb395/user/hash.py#L14-L29)

*DB_NAME, DB_USER, DB_PASSWORD* - Constants for [database creation](https://github.com/romashovdmitry/longevity_user_system/blob/8a33f0f546667c2d7e5718156acef2992c8f7532/longevity/settings.py#L76-L85)

*SECRET_KEY* - standart secret_key for Django project

3. Run docker-compose 

```
docker-compose up
```

4. Create a superuser to access the Django admin panel
