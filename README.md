xuemei
======

Web server for image host

install django 1.5rc

Todo: install django restful framework. test it.

pip install djangorestframework 

$sudo apt-get update

$sudo apt-get install postgresql

sudo apt-get build-dep python-psycopg2
pip install psycopg2

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
locale-gen en_US.UTF-8
dpkg-reconfigure locales

sudo -u postgres createuser --superuser <someuser> -P
sudo -u postgres createdb -O xuemei xuemeidb

sudo vi /etc/postgresql/9.1/main/pg_hba.conf

local all all md5

pip install django-social-auth

Todo: integrate upyun SDK, offer upload API.

Todo: celery + redis for message queue.
 pip install -U celery-with-redisi


TODO: nginx + supervisord + django 1.5 wsgi
pip install uwsgi
apt-get install nginx

uwsgi --socket 127.0.0.1:8000 --chdir /home/ubuntu/xuemei/mysite --wsgi-file mysite/wsgi.py --processes 4 --threads 2 --stats 127.0.0.1:9191 --virtualenv /home/ubuntu/xuemei/env

pip install django-socketio

pip install pinax-theme-bootstrap-account

pip install django-userena
http://docs.django-userena.org/en/latest/installation.html
sudo pip install -U PIL

pip install sentry //5.4.5
need celery > 3.0.17

sudo apt-get install postfix //for sentry email

pip install django-follow https://github.com/caffeinehit/django-follow

install geodjango https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/

pip install django-filter

pip install django-taggit

pip install django-voting
