# ecommerce

This is a project that represents a technology ecommerce API Tes. This is a version test that can be extended for a production test.

A minimal Django app that implements models that can to do operations into ecommerce API.



****The app implements these models:****

 - ``User``: Model base for create system's user.
 - ``LogSystem``: The model that register wheather occur actions from user.
 - ``Client``: Model for all clients. (NOTE: Is not used for create Admin user).
 - ``Brand``: Model for register the product brand.
 - ``ExtraProductType``: Model created to register all products extra characters.
 - ``ProductType``: Model created to register all product type. Ex: "Placa mãe, Processador, etc.."
 - ``Product``: Model created to register all products. (Note: It receive the typeproduct, brand and extra_product_types)
 - ``Request``: Model created to register all requests of clients.

Dependencies
------------
- Python 2.7 or 3.4+
- Django 1.11+
- For the API module, Django REST Framework 3.7+ is required.
- For run the application, it's need have docker installed

Setup
------------

First you have to do a download of the docker image:

    `git clone https://gitlab.com/georgericardo26/ecommerce.git`

After, you will init the container service:

    `sudo docker-compose up`

Authentication
------------

For use the authentication endpoint you must provide a json object with the following informations:

``endpoint``: `http://0.0.0.0:8000/api/v1/auth`

**Json Object:**
 {<br>
    &nbsp;&nbsp;"client_id": "ysP8nLr1RJuUJkWls85INtRk0YmLAZgTNNbMAYM3",<br>
    &nbsp;&nbsp;"client_secret": "rUwoNIm05LwvvnrmSJvNmWNWzrLS70C2OTLVu51bDmX9CEeiSvzZGWg3shQbINiAo1DsWWtde79HH0AAiWmqWbjsJEKnsST7O2i37Sn9Dcg5ka4BTb5k5trJvwG15Q8U",<br>
	&nbsp;&nbsp;"username": "admin",<br>
	&nbsp;&nbsp;"password": "admin"<br>
}


CREDENTIALS ADMIN TEST:

**username**:`admin`
**password**: `admin`


NOTE: For generate access_token for client user, you must first create a client user. This endpoint not receive access token.


Documentation:
------------
For all the others request created for this project you must access this link here:

We are using 2 libraries: ***Swagger**** and **Redoc****

`Local Swagger`: http://localhost:8000/api/v1/swagger/<br>
`Local Redoc`: http://localhost:8000/api/v1/redoc/<br>
<br><br>
`Server Swagger`: Soon...<br>
`Server Redoc`: Soon...<br>

Django Admin:
------------

You can use this credentials test provided for access the Django admin panel

`Local`: http://localhost:8000/admin/<br>
`Server`: Soon...<br>


