HOST=127.0.0.1
PROJECT_NAME=project

freeze:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

migrate:
	python $(PROJECT_NAME)/manage.py makemigrations && python $(PROJECT_NAME)/manage.py migrate

test:
	python $(PROJECT_NAME)/manage.py test --verbosity 2 ./$(PROJECT_NAME)

run:
	python $(PROJECT_NAME)/manage.py runserver

docker-prod: freeze
	docker build \
		--no-cache \
		--file=Dockerfile \
		--tag=project ./
	docker run \
		--detach=true \
		--publish=8000:8000 \
		project

docker-local: freeze
	docker build \
		--no-cache \
		--file=Dockerfile.local \
		--tag=project_local ./
	docker run \
		--detach=true \
		--publish=8000:8000 \
		project_local

# Delete all migrations file
clean-migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc" -delete