all:
	docker-compose up -d

build:
	docker-compose build

stop:
	docker-compose stop

down:
	docker-compose down