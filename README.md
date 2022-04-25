# Backend Homework API Rest

API Rest project, using Django and a movie topic for CRUD operations.
http://davidfcr.pythonanywhere.com/

## Installation on local machine

Tested on docker version 20.10.12
Download the repo, and run the following commands:

    1. docker-compose build
    2. docker-compose up

Once the installation is finish and the docker is up, the project can be access in the http://0.0.0.0:8080 (base_url) localhost direction.

## Documentation of the API

Can download the json documentation and import into Postam using http://davidfcr.pythonanywhere.com/swagger.json

A Swagger page was created with the detailed information for the API's on the root page.

1. Use the /api/user/register endpoint to create a new user
2. Once is register, use the /api/user/register
3. You will receive a token to use as Bearer token authorization for the film endpoints
4. Use any of the film API endapoint with the Authorization bearer token in the header
 ex: 
 curl --location --request GET 'http://davidfcr.pythonanywhere.com/api/film/all' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImRhdmlkY2FyZGVuYXNyYWlnb3NhQGdtYWlsLmNvbSIsImV4cGlyYXRpb24iOiIyMDIyLTA0LTI1VDA2OjMxOjAzIn0.G2DtM_V1Yiz6-vdpQWnOPRIo27mhClUAjz2hrJMMAv0' \
--data-raw ''

## Random number API

A random number GET endpoint was included into this project.
{base_url}/api/user/number
