xuemei
======

Web server for image host

install django 1.5rc

Todo: install django restful framework. test it.

pip install djangorestframework 

$sudo apt-get update

$sudo apt-get install postgresql

export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
locale-gen en_US.UTF-8
dpkg-reconfigure locales

sudo -u postgres createuser --superuser <someuser> -P

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

