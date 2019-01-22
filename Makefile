export FLASK_APP=app

all: run

hello:
	env FLASK_ENV=development FLASK_APP=hello.py flask run --host=0.0.0.0

run-simple:
	env FLASK_ENV=development FLASK_APP=app_simple.py flask run --host=0.0.0.0

run:
	env FLASK_ENV=development flask run --host=0.0.0.0

run-secure:
	env FLASK_ENV=development FLASK_APP=app_secure.py flask run --host=0.0.0.0
