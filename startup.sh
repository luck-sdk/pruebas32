#!/bin/bash

echo "Instalando ODBC..."

apt-get update
apt-get install -y curl gnupg2

curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17

echo "Iniciando Gunicorn..."
gunicorn --bind=0.0.0.0:8000 --workers 2 app:app
