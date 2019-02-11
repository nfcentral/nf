all: docker cachedocker

docker:
	DOCKER_BUILDKIT=1 docker build -t theiced/nf -f dockers/Dockerfile .

cachedocker:
	DOCKER_BUILDKIT=1 docker build -t theiced/nfcache -f dockers/Dockerfile.cache .
