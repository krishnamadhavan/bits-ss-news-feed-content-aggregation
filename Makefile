pytest:
	coverage run -m pytest

shell:
	docker-compose exec django sh -c "python manage.py shell"

makemigrations:
	docker-compose exec django sh -c "python manage.py makemigrations"

migrate:
	docker-compose exec django sh -c "python manage.py migrate"
