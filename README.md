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
