#!/bin/sh

origin=$(pwd)
nf_root=$(dirname $(realpath $0))
command=$1

case ${command} in
    selfbuild)
        cd ${nf_root}
        docker build -t theiced/nf -f dockers/Dockerfile.nf .
        docker build -t theiced/nfcache -f dockers/Dockerfile.nfcache .
        cd ${origin}
        ;;
    build)
        docker run --rm -d --name nfcache -v nfcache:/data -p 873:873 theiced/nfcache
        docker-compose -f .nf/docker-compose.yml --project-directory . build
        docker stop nfcache
        ;;
    up)
        docker run --rm -d --name nfcache -v nfcache:/data -p 873:873 theiced/nfcache
        docker-compose -f .nf/docker-compose.yml --project-directory . up
        docker stop nfcache
        ;;
    start)
        docker-compose -f .nf/docker-compose.yml --project-directory . start
        ;;
    stop)
        docker-compose -f .nf/docker-compose.yml --project-directory . stop
        ;;
    release)
        docker run --rm -d --name nfcache -v nfcache:/data -p 873:873 theiced/nfcache
        sh .nf/nf-release
        docker stop nfcache
        ;;
    *)
        docker run --rm -v $(pwd):/project theiced/nf $*
        ;;
esac
