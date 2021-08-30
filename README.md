Project name: RemindMe
-
Description:
-
User create reminders and receives email notifications on particular date-time.

Main features:
-
- sign-up
- email activation
- jwt autorization
- permissions
- retreive profile/change email or pass
- crud reminders
- crud reminder category
- filter reminders by category or remind date
- search reminder
- send email notifications to user at particular date-time
- add additional emails to reminder notification list

Technologies used:
-
- django
- django rest framework
- rest: api
- celery
- postgresql
- redis
- rabbitmq

How to setup the projects:
-
1. setup enviroment variables in PyCharm using .env file
2. activate local evironment and install all packages: 
- run in terminal 'pipenv shell'
- run in terminal 'pipenv install'
3. run docker containers
- install Docker
- run in terminal 'docker-compose -f docker-compose-dev.yml up'
4. Run server
5. Run celery
6. Done! :)


Endpoints:
-
app name: authentication

http://127.0.0.1:8000/v1/auth/	# obtail JWT

http://127.0.0.1:8000/v1/auth/refresh/	# refresh JWT	

http://127.0.0.1:8000/v1/auth/verify/	# verify JWT	

http://127.0.0.1:8000/v1/auth/sign-up/	# user sign-up

http://127.0.0.1:8000/v1/auth/activate/	# user activation

***
app name: notifications

http://127.0.0.1:8000/v1/notifications/email/	# user add email to recipient list

***
app name: reminders

http://127.0.0.1:8000/v1/reminders/category/	# CRUD reminder category

http://127.0.0.1:8000/v1/reminders/	# CRUD reminder

***
app name: user_profile

http://127.0.0.1:8000/v1/profile/		# retreive profile

http://127.0.0.1:8000/v1/profile/password/change/	# change profile password

http://127.0.0.1:8000/v1/profile/email/	# change profile email

http://127.0.0.1:8000/v1/profile/deactivate/	# deactivate user profile
