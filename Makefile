run:
	python3 manage.py makemigrations users
	python3 manage.py makemigrations content
	python3 manage.py migrate
	uvicorn bitpin.asgi:application --host 0.0.0.0 --port 8000