# livingarchive
Wagtail Living Archive
# Place install notes here - how to setup Wagtail server
python3 -m venv
source env/bin/activate
pip install -r requirements.txt
add .env file to livingarchive/settings/ with API_KEY=
# To update database
python manage.py makemigrations
python manage.py migrate 
python manage.py runserver