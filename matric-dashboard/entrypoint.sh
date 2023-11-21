#!/usr/bin/env bash

echo "Performing postgres upgrade"
flask db migrate
flask db upgrade

echo "Launching Flask"
flask run --host 0.0.0.0