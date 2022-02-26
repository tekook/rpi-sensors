#!/bin/bash
pip install virtualenv && \
virtualenv ./venv && \
source ./venv/bin/activate && \
pip install -r setup/requirements.txt && \
deactivate && \
ln -s $PWD/setup/rpi-sensors.service /etc/systemd/system/rpi-sensors.service && \
systemctl daemon-reload && \
chown -R www-data:www-data $PWD && \
ln -s $PWD/setup/rpi-sensors.conf /etc/nginx/sites-enabled/rpi-sensors.conf
