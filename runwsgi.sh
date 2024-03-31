source ./env/bin/activate
#setup
#python3 manage.py makemigrations
#python3 manage.py migrate
#python3 manage.py runserver 127.0.0.1:8006
# if get database readonly, you may need to change owner chown mail:mail db.sqlite3 
#to refresh env recreate and run 
#source ./env/bin/activate
#pip install -r requirements.txt --no-cache-dir

#uwsgi --master --socket 127.0.0.1:8006 --uid mail --logto ./prodlivingarchive.log --chdir ./ --env DJANGO_SETTINGS_MODULE=livingarchive.settings.production --wsgi-file ./livingarchive/wsgi.py  --chmod-socket=666
#uwsgi --master --socket /tmp/livingarchive.sock --chdir ./ --env DJANGO_SETTINGS_MODULE=livingarchive.settings.production --wsgi-file ./livingarchive/wsgi.py  --chmod-socket=666
#uwsgi --master --socket /tmp/livingarchive.sock --chdir ./ --env DJANGO_SETTINGS_MODULE=livingarchive.settings.production --wsgi-file ./livingarchive/wsgi.py  --chmod-socket=666
env/bin/uwsgi --master --socket /tmp/laal.sock --chdir ./ --uid mail --logto ./prodlivingarchive.log --env DJANGO_SETTINGS_MODULE=livingarchive.settings.production --wsgi-file ./livingarchive/wsgi.py  --module "django.core.handlers.wsgi:WSGIHandler()" --chmod-socket=666
env/bin/uwsgi --master --socket /tmp/laal.sock --chdir ./ --uid mail --logto ./prodlivingarchive.log --env DJANGO_SETTINGS_MODULE=livingarchive.settings.production --wsgi-file ./livingarchive/wsgi.py  --module "django.core.handlers.wsgi:WSGIHandler()" --chmod-socket=666


