rm -rf data/db.sqlite3
rm -rf static
python manage.py collectstatic
python manage.py makemigrations
python manage.py migrate
python manage.py flush --noinput
python initdb.py
python manage.py runserver
