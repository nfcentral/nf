VERSION=$(shell cat VERSION)

all: build

build:
	docker run --rm -d --name nfcache-latest -v nfcache:/data -p 873:873 nfcentral/nfcache:latest
	DOCKER_BUILDKIT=1 docker build --network=host -t nfcentral/nf:latest .
	docker stop nfcache-latest
	docker tag nfcentral/nf:latest nfcentral/nf:$(VERSION)

release: build
	docker push nfcentral/nf:$(VERSION)
	docker push nfcentral/nf:latest
