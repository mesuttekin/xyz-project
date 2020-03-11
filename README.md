#### Requirements for the project:
* A user signs up using the details
    * Unique Email
    * First Name
    * Surname
    * Password
* The user logs in using their email and password
    * Sign up and login should be secure on a token based system
    * To do any functionality a secure token is required.
* The user creates a new project.  The project creator is the owner
* A user can be part of many projects
* The user can view a list of projects that are already created
* A project owner can add a registered user to a project using their email address.
* If a user is part of a project then they can access the project
* When in a project a user can add a device to the project (for this a device is a record consisting of a 5 digit serial number and a Name)
* User that have access to a project can see a list of devices.
    * A device can be part of many projects

#### Prerequisites:
This project is developed with Python. So before start please install Python if you don't have it already

* Python3
* PIP
* Virtualenv
```
brew install python3
python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv
```

Below python features and extensions are used within the project. 
* Flask-Bcrypt: A Flask extension that provides bcrypt hashing utilities for your application.
* Flask-Migrate: An extension that handles SQLAlchemy database migrations for Flask applications using Alembic. The database operations are made available through the Flask command-line interface or through the Flask-Script extension.
* Flask-SQLAlchemy: An extension for Flask that adds support for SQLAlchemy to your application.
* PyJWT: A Python library which allows you to encode and decode JSON Web Tokens (JWT). JWT is an open, industry-standard (RFC 7519) for representing claims securely between two parties.
* Flask-Script: An extension that provides support for writing external scripts in Flask and other command-line tasks that belong outside the web application itself.
* Namespaces (Blueprints)
* Flask-restplus
* UnitTest

Please follow below steps to install prerequisites.
```
git clone https://github.com/mesuttekin/xyz-reality-project.git
cd xyz-reality-project
python3.8 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
#### Database Models and Migration:
To perform the migration please run the following commands on the project root directory:

1. Initiate a migration folder using init command for alembic to perform the migrations.
```
python manage.py db init
```
2. Create a migration script from the detected changes in the model using the migrate command. This doesn’t affect the database yet.

```
python manage.py db migrate --message 'initial database migration'
```
3. Apply the migration script to the database by using the upgrade command

```
python manage.py db upgrade
```
If everything runs successfully, you should have a new sqlLite database
xyz_reality_main.db file generated inside the main package.

 Note: Each time the database model changes, repeat the migrate and upgrade commands

#### Run Application:

You can run the application with the command below in the project root directory

```
python manage.py run
```

#### Test Application:

You can run the unit tests of the application with the command below in the project root directory

```
python manage.py test
```