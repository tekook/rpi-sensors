#!/bin/bash
systemctl stop irsend.service && \
rm /etc/systemd/system/irsend.service && \
systemctl daemon-reload && \
rm /etc/nginx/sites-enabled/irsend.conf && \
rm -R ./venv
