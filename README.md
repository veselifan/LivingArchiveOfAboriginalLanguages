# livingarchive
Wagtail Living Archive
# Place install notes here - how to setup Wagtail server

python3 -m venv

source env/bin/activate

pip install -r requirements.txt

add .env file to livingarchive/settings/ with API_KEY=

#
env\Scripts\activate    #activating in windows
python manage.py runserver

# To update database
python3 manage.py makemigrations

python manage.py migrate 

python manage.py runserver
