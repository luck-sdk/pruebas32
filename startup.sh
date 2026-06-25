#!/bin/bash

echo "🔧 Instalando dependencias ODBC..."

apt-get update -y
apt-get install -y curl gnupg2 unixodbc unixodbc-dev

curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list > /etc/apt/sources.list.d/mssql-release.list

apt-get update -y
ACCEPT_EULA=Y apt-get install -y msodbcsql17

echo "🚀 Iniciando Gunicorn..."

gunicorn --bind=0.0.0.0:8000 --workers=2 --threads=4 --timeout=120 app:app