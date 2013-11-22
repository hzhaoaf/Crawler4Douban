NG Backend
==========

Our backend is powered by Django, WSGI and Apache.

Please see the official simple installation and configurations references:
*   [modwsgi-Installation On Linux](http://code.google.com/p/modwsgi/wiki/InstallationOnLinux#Installation_On_Linux)
*   [modwsgi-Integration With Django](http://code.google.com/p/modwsgi/wiki/IntegrationWithDjango)
*   [How to deploy with WSGI](https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/#how-to-deploy-with-wsgi)
*   [How to use Django with Apache and mod_wsgi](https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/modwsgi/)

For Django part, I recommend again the official guide:
*   [Quick install guide](https://docs.djangoproject.com/en/1.4/intro/install/)
*   [Writing your first Django app](https://docs.djangoproject.com/en/1.4/intro/tutorial01/)
*   [The Django Book](http://www.djangobook.com/en/2.0/index.html)

Though there are not so many 5-minute tutorials, the official document and `The Django Book` both did a awesome job!!!

Installation On a Debian Wheezy machine is tricky using `apt-get` really, something like:

    sudo apt-get install python-django
    sudo apt-get install python-mysqldb
    sudo apt-get install libapache2-mod-wsgi

To simply start a project,

    django-admin startproject your_project_name

To debug on localhost utilizing Django's lightweight http server,
    
    python manage.py runserver

To make your database begin to work,

    vi your_project_name/your_project_name/setting.py
    python manage.py syncdb

To start an app,

    python manage.py startapp your_app_name

All left to you is to config your URL router and implement your views, also cheers:-)

**Note:**

Please refer to the official guide since I got very confused when I try to refer to some blogs, basically due to they are using **OLD** Django and **deprecated** mod_python. Trust me, it's worth your time!

**Kindly Hint:**

Our backend has moved to a new repository called [MovieSearchService](https://github.com/PhoenixZhao/MovieSearchService).
