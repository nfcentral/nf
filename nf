#!/bin/sh

set -e

if [ "0" = "$#" ]; then
    docker run --rm -v "$(pwd)":/project theiced/nf
    exit 1
fi

command=$1
shift

if [ "--help" = "$1" ]; then
    docker run --rm -v "$(pwd)":/project theiced/nf ${command} $1
    exit 1
fi

if [ "new" = "${command}" ]; then
    if [ "0" = "$#" ]; then
        docker run --rm -v "$(pwd)":/project theiced/nf ${command} $*
        exit 1
    fi
    name=$1
    shift
    if [ -d "${name}" ]; then
        echo "Error: directory ${name} already exists. "
        exit 1
    fi
    mkdir -p dir
    docker run --rm -v "$(pwd)/${name}":/project theiced/nf ${command} ${name} $*
    exit 0
fi

if [ -f ".nf/commands/${command}" ]; then
    sh .nf/commands/${command} $*
    exit 0
fi

docker run --rm -v "$(pwd)":/project theiced/nf ${command} $*
