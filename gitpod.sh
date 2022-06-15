pip install -r requirements.txt
python manage.py db upgrade
python manage.py dbseed
python manage.py runserver