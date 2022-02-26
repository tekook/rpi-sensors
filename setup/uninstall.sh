#!/bin/bash
systemctl stop rpi-sensors.service ; \
systemctl disable rpi-sensors.service ; \
rm /etc/systemd/system/rpi-sensors.service && \
systemctl daemon-reload && \
rm /etc/nginx/sites-enabled/rpi-sensors.conf && \
rm -R ./venv
