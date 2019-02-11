#!/bin/sh

origin=$(pwd)
nf_root=$(dirname $(realpath $0))
command=$1
shift

case ${command} in
    selfbuild)
        cd ${nf_root}
        docker build -t theiced/nf -f dockers/Dockerfile .
        cd ${origin}
        ;;
    build)
        docker-compose build
        ;;
    up)
        docker-compose up
        ;;
    *)
        docker run --rm -v $(pwd):/project theiced/nf $*
        ;;
esac
