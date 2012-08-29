django-authy-admin
==================

A drop in replacement for django's default admin site that provides two-factor authentication via authy's REST API.

Installation
============

Install the latest stable version of `django-authy-admin`

    easy_install django-authy-admin

    
Add `authy_admin` to your `INSTALLED_APPS` after `django.contrib.admin`:

    INSTALLED_APPS = (
        ...
        'django.contrib.admin',
        'authy_admin',
        ...
    )

ADD `AUTHY_API_KEY` to `settings.py`:

    AUTHY_API_KEY = '...' 
    
    (you can get your free API key by signing up at authy.com)

Use `manage.py` to create database table used by `authy_admin`:

    python manage.py syncdb
    
Visit your site's admin, if you are prompted to login use your usual username and password but leave `Authy Token` blank.

Add an `Authy Admin User` for a staff member that wants two-factor authentication.

Next time the user visits the admin he or she will be required to login with a one time password provided by authy.com.