# API Documentation

## Overview

The API is designed to create invoices and approve them. The API is built using Django Rest Framework and provides endpoints for creating and update providers and invoices.

## Endpoints


### Provider Endpoints
#### To create a provider
- **URL**: `/api/providers`
- **Method**: `POST`
- **Description**: This endpoint is used to create new providers.
- **Headers**:
  - **Authorization**: `Bearer <token>`
  - **Content-Type**: `application/json`
- **Request Body**:
  - **Content-Type**: `application/json`
  - **Schema**:
    ```json
    {
        "name": "Grupo AJE",
        "address": "Jiron Bolognesi 123, Surco",
        "phone_number": "51981042222"
    }
    ```
  - **Fields**:
    - [`name`](string): The name of the provider.
    - [`address`](string): The adress of the provider.
    - [`phone_number`](integer): The number of the provider.
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**:
    ```json
    {
        "id": 7,
        "user": 1,
        "name": "Grupo AJE",
        "address": "Jiron Bolognesi 123, Surco",
        "phone_number": "51981042222"
    }
    ```

#### Provider list

- **URL**: `/api/providers`
- **Method**: `GET`
- **Description**: This endpoint is used to retrieve providers list
- **Headers**:
  - **Authorization**: `Bearer <token>`
  - **Content-Type**: `application/json`
- **Request Body**:
  - **Content-Type**: `application/json`.
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**:
    ```json
    [
        {
            "id": 1,
            "user": 1,
            "name": "Grupo AJE",
            "address": "Jiron Bolognesi 123, Surco",
            "phone_number": "51981042222"
        },
        {
            "id": 2,
            "user": 1,
            "name": "Backus",
            "address": "Jiron castilla 123, San Borja",
            "phone_number": "981041111"
        },
    ]
    ```


### Invoice Endpoints
#### To create a invoice
- **URL**: `/api/invoices`
- **Method**: `POST`
- **Description**: This endpoint is used to create new invoices.
- **Headers**:
  - **Authorization**: `Bearer <token>`
  - **Content-Type**: `application/json`
- **Request Body**:
  - **Content-Type**: `application/json`
  - **Schema**:
    ```json
    {
        "state": "PENDING",
        "provider": "Grupo AJE",
        "items": [
            {
                "name": "gaseosa",
                "quantity": 15,
                "price": "21.50"
            },
            {
                "name": "chupetin",
                "quantity": 12,
                "price": "42.50"
            }
        ]
    }
    ```
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**:
    ```json
    {
        "id": 10,
        "user": 1,
        "provider": "Grupo AJE",
        "state": "PENDING",
        "items": [
            {
                "name": "gaseosa",
                "quantity": 15,
                "price": "21.50"
            },
            {
                "name": "chupetin",
                "quantity": 12,
                "price": "42.50"
            }
        ],
        "total_cost": 832.5
    }
    ```

#### To retrieve a invoice
- **URL**: `/api/invoices/<id>`
- **Method**: `GET`
- **Description**: This endpoint is to retrieve a invoice by its id
- **Headers**:
  - **Authorization**: `Bearer <token>`
  - **Content-Type**: `application/json`
- **Path parameters**:
  - **id**: The unique identifier of the invoice
- **Response**:
  - **Status Code**: `200 OK`
  - **Body**:
    ```json
    {
        "id": 7,
        "user": 1,
        "provider": "Backus",
        "state": "REJECTED",
        "items": [
            {
                "name": "Sporade",
                "quantity": 12,
                "price": "10.00"
            }
        ],
        "total_cost": 120.0
    }
    ```
## Exceptions

- **RequestValidationError**: Raised when the request body does not conform to the expected schema.
  - **Status Code**: `400 Bad Request`
  - **Response**:
    ```json
    {
        "detail": "JSON parse error - Expecting value: line 3 column 16 (char 32)"
    }
    ```
    ```json
    {
        "state": [
            "\"PENDING123\" is not a valid choice."
        ]
    }
    ```

# Setup

- [Visual Studio Code](https://code.visualstudio.com/Download)
- Python 3.9.13

VSCode Extension:

- Black


## Init repo

Create virtual environment
```bash
python3 -m venv .venv
```

To activate virtual environment
```bash
source .venv/bin/activate
```

To install dependencies
```bash
pip install -r requirements.txt
```

## DataBase

To simulate the database locally, run the following commands:

```shell
python manage.py makemigrations
python manage.py migrate
```

## Simulations

To simulate server locally, run the django server with:

```shell
python manage.py runserver
```
