all: build

build:
	../.venv/bin/pelican

run: build
	../.venv/bin/twistd -no web --path ./output

publish:
	../.venv/bin/pelican -s publishconf.py
	s3_website push
