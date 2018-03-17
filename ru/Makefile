all: build

build:
	pelican

run: build
	twistd -no web --path ./output

publish:
	pelican -s publishconf.py
	s3_website push
