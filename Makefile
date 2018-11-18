all: build
	docker-compose build

build:
	docker-compose build

start-ru:
	docker-compose stop pelican-en
	docker-compose up -d pelican-ru
	open http://localhost:8000/blog/

start-en:
	docker-compose stop pelican-ru
	docker-compose up -d pelican-en
	open http://localhost:8000/blog/

stop:
	docker-compose stop

publish-ru:
	docker-compose run --rm pelican-ru pelican -D -s publishconf.py -o /output content
	docker-compose run --rm s3-website-ru s3_website push

publish-en:
	docker-compose run --rm pelican-en pelican -D -s publishconf.py -o /output content
	docker-compose run --rm s3-website-en s3_website push
