assignment-dashboard-backend
=======================

**assignment-dashboard-backend** is a project that provides a django database
backend that works with **MySQL** to keep track of courses, their assignments, and due dates.

Installation
------------
1. Download zip or clone repo
2. Run `pip install -r requirements.txt`

Database Setup
------------
1. In MySQL workbench create a new connection & database to hold the data
2. Create a local_settings.py file (folder structure: 'assignmentdashboard\assignmentdashboard\local_settings.py')
   local_settings.py file contents:
   ```
    from django.core.management.utils import get_random_secret_key

    SECRET_KEY = get_random_secret_key

    DATABASES = {
        'default': {
            'ENGINE': 'mysql.connector.django',
            'NAME': 'database_name',
            'USER':'root',
            'PASSWORD':'your_password',
            'HOST':'your_host',
            'PORT':'your_port',
            'OPTIONS': {
                'autocommit': True
            }
        }
3. Navigate to 'assignmentdashboard\assignmentdashboard' in command line and run `python manage.py migrate`
4. Run `python manage.py createsuperuser` to generate admin profile

Usage
------------
1. Run backend using `python manage.py runserver`
2. Django admin interface: http://127.0.0.1:8000/admin/

API
------------
For API call examples see assignment-dashboard-frontend: https://github.com/aschmidt2020/assignment-dashboard-frontend
