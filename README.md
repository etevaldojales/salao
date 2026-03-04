Sempre excluir a venv


py -m venv venv
.\venv\Scripts\activate.ps1
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Ordem de instalação:

- py -m venv venv
- .\venv\Scripts\activate.ps1
- python.exe -m pip install --upgrade pip
- python -m pip install django
- django-admin startproject projeto .((já tem
- python manage.py startapp agendamentos ((já tem
- python -m pip install mysqlclient
- python -m pip install django-soft-delete
- python -m pip install pycasbin
- 
- python manage.py runserver

SUPERUSER:

dono_admin
