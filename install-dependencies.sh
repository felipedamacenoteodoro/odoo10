#!/bin/bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends locales ca-certificates nano wget git mercurial screen htop curl openssh-client node-less node-clean-css tig binutils build-essential bzr ca-certificates cpp cups gcc dpkg-dev fontconfig fontconfig-config gir1.2-glib-2.0 git git-core git-man tar zip gzip zlib1g sudo libffi-dev expect-dev libxml2-dev libxslt-dev gcc python2.7-dev libevent-dev libsasl2-dev libldap2-dev libpq-dev libpng12-dev libjpeg-dev xfonts-75dpi xfonts-base postgresql-client* python-pip 
sudo pip install virtualenv
sudo locale-gen en_US en_US.UTF-8 pt_BR.UTF-8
echo "CURL iniciando..."
sudo curl -o wkhtmltox.deb -SL http://nightly.odoo.com/extra/wkhtmltox-0.12.1.2_linux-jessie-amd64.deb
echo '40e8b906de658a2221b15e4e8cd82565a47d7ee8 wkhtmltox.deb' | sha1sum -c - 
sudo dpkg --force-depends -i wkhtmltox.deb
sudo apt-get -y install -f --no-install-recommends
