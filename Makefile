all: build

build:
	DOCKER_BUILDKIT=1 docker build --network=host -t nfcentral/nf .
