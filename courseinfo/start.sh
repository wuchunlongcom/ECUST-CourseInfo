rm -rf data/db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py flush --noinput
python initdb.py
python manage.py runserver
#python manage.py runserver 192.168.31.14:8080
