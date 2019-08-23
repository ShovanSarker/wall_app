# Wall App

This application was built for an interview test for!

### The problem

Wall App is a website that allows users to register, login, and write on a wall.

Below are the minimum requirements.  You are free to add any additional features you like.

- Registration and Login: Anonymous users can create a new user and this new user receives a welcome email. New users can then log in.
- Wall (authed):  After logging in, a user can post messages on the site-wide wall, similar to a facebook wall except there is only 1 wall for the entire site.  
- Wall (guest): Guests as well as authed users can see all of the messages on the wall.
- Write tests to confirm the functionality of the above requirements  

Note: a lot of the finer details are left out of this description, do whatever you think would make sense.  You are being judged on code and API design, not on how useful or interesting you make the app.  If you do however find a way to make it interesting, that’s a bonus!
#### Tech Info
- Backend: REST API (python or javascript, preferably Django with Django REST Framework)
- Frontend: AJAX-based website or native app (e.g. using React, Angular, React Native, iOS, Android)

Backend and frontend should be completely separate apps, i.e. the Django backend does not render any html pages for the frontend.

### Prerequisites

The liraries used in this project are
* certifi==2019.6.16
* chardet==3.0.4
* Django==2.2.4
* django-cors-headers==3.1.0
* djangorestframework==3.10.2
* idna==2.8
* pytz==2019.2
* requests==2.22.0
* sqlparse==0.3.0
* urllib3==1.25.3


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required libraries.

```bash
pip install -r requirements.txt
```
or installing the required libraries manually by 
```bash
pip install Django
...
```

## Usage
After the required libraries installed, go inside the project directory and check if the ```manage.py``` file is there. If it is there run the following code:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```
these commands will update the database structure(if necessary) and run the service on [localhost](http://localhost:8000) on 8000 port.

### WIKI
More details about the API is documented at [this wiki](https://github.com/ShovanSarker/wall_app/wiki)

## License
[MIT](https://choosealicense.com/licenses/mit/)
