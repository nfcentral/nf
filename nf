#!/bin/sh

set -e

if [ -z ${NF_VERSION} ]; then
    if [ -z "$(docker images -q nfcentral/nf:active)" ]; then
        NF_VERSION="latest"
    else
        NF_VERSION="active"
    fi
fi

if [ -z "$(docker images -q nfcentral/nf:${NF_VERSION})" ]; then
    docker pull nfcentral/nf:${NF_VERSION}
fi

if [ "0" = "$#" ]; then
    docker run --rm -v "$(pwd)":/project nfcentral/nf:${NF_VERSION}
    exit 1
fi

command=$1
shift

if [ "--help" = "$1" ]; then
    docker run --rm -v "$(pwd)":/project nfcentral/nf:${NF_VERSION} ${command} $*
    exit 1
fi

if [ "selfupgrade" = "${command}" ]; then
    if [ "0" != "$#" ] && [ "1" != "$#" ]; then
        docker run --rm -v "$(pwd)":/project nfcentral/nf:${NF_VERSION} ${command} $*
        exit 1
    fi
    if [ "0" = "$#" ]; then
        newversion="latest"
    else
        newversion=$1
    fi
    docker pull nfcentral/nf:${newversion}
    if [ "latest" = "${newversion}" ]; then
        if [ ! -z "$(docker images -q nfcentral/nf:active)" ]; then
            docker rmi nfcentral/nf:active
        fi
    else
        docker tag nfcentral/nf:${newversion} nfcentral/nf:active
    fi
    docker run --rm -v "$(pwd)":/project nfcentral/nf:${newversion} install >"$0.upgrade"
    chmod +x "$0.upgrade"
    mv "$0.upgrade" "$0" && exit
fi

if [ "new" = "${command}" ]; then
    if [ "0" = "$#" ]; then
        docker run --rm -v "$(pwd)":/project nfcentral/nf:${NF_VERSION} ${command} $*
        exit 1
    fi
    name=$1
    shift
    if [ -d "${name}" ]; then
        echo "Error: directory ${name} already exists."
        exit 1
    fi
    mkdir -p dir
    docker run --rm -v "$(pwd)/${name}":/project nfcentral/nf:${NF_VERSION} ${command} ${name} $*
    exit 0
fi

if [ -f ".nf/commands/${command}" ]; then
    NF_VERSION=${NF_VERSION} sh .nf/commands/${command} $*
    exit 0
fi

docker run --rm -v "$(pwd)":/project nfcentral/nf:${NF_VERSION} ${command} $*
