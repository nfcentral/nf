all: build

build:
	DOCKER_BUILDKIT=1 docker build -t theiced/nf .
