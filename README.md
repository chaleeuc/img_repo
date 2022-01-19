# Shopify Challenge

Tries to solve challenge at  [https://docs.google.com/document/d/1eg3sJTOwtyFhDopKedRD6142CFkDfWp1QvRKXNTPIOc/edit](https://docs.google.com/document/d/1eg3sJTOwtyFhDopKedRD6142CFkDfWp1QvRKXNTPIOc/edit)

using django framework, I decided to make an ecommerce like application, where admin can add product and related images from backend, and regular user can and regular users can add them to cart, and pay using paypal.

Python needs to be installed in ordered to run the application

## Set up for running on local server

1. Download the code, create virtual environment inside the folder using python -m venv venv 
2. Activate the virtual environment using ./venv/Scripts/Activate (I am using windows, this process may differ for mac or linux users) 
3. Install required libraries using pip install -r requirements.txt

## Setting up database

1. Since the application is running on local server, we need to set up database by running python manage.py makemigrations, then python manage.py migrate 
2. Application is not equipped to add images from frontend, yet.. you will require an admin user to access the backpage and add the item/images manually for now 
	2.1. create superuser using python manage.py createsuperuser 
	2.2. now you can access the database and add items and images at localhost:8000/admin/ (slash is required at the end of admin, login using email used for signup) 
3. Add @ Shop categories, product type, and product 
	3.1. there are stock wedding photos in sample_images folder 
	3.2. while setting up products, one of the image will need to be set as featured (click on the top one), for item to shown up on the index of webpage 
	3.3. Once images are added, images files will be moved to media/images folder to be accessed from the website, if the application is deployed, we can set up the application to use amazon s3 to securely store the images 
	
## Setting up user / And payment process
1. Users can register, and login to the application, its fine to use the admin user as well 
2. Go to Homepage, and add to cart whatever item you have added into db 
3. Go to cart, and checkout, you can use paypal's sandbox account associated with the application to pay 
	- sandbox account: <span>sb-1a1hi12017074<span>@personal.example.com</span></span>
	- sandbox password: 1U%bY22:  
5. if payment is successful, user will be able to notice post status on console, and see the order shown up on dashboard/orders
