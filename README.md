# (General) Disarray

Django based task manager

## Dev Setup ##

    $ python local/setup.py --distribute venv
    $ . venv/bin/activate
    $ pip install -r REQUIREMENTS
    $ cp local/settings.py.template local/settings.oy
    $ $EDITOR local/settings.py # wth local/settings.py.template and fill in ...
    $ python manage.py syncdb

## Run Server ##

    $ python manage.py runserver <port>
