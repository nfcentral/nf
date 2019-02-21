VERSION=$(shell cat VERSION)

all: build

build:
	DOCKER_BUILDKIT=1 docker build --network=host -t nfcentral/nf:latest .
	docker tag nfcentral/nf:latest nfcentral/nf:$(VERSION)

release: build
	docker push nfcentral/nf:$(VERSION)
	docker push nfcentral/nf:latest
