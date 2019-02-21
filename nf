#!/bin/sh

set -e

if [ -z ${NF_IMAGE} ]; then
    if [ -f "nf.nffreeze" ]; then
        NF_IMAGE=$(cat nf.nffreeze | awk -F ":" '{ print $1 }')
    else
        NF_IMAGE="nfcentral/nf"
    fi
fi

if [ -z ${NF_VERSION} ]; then
    if [ -f "nf.nffreeze" ]; then
        NF_VERSION=$(cat nf.nffreeze | awk -F ":" '{ print $2 }')
    else
        NF_VERSION="latest"
    fi
fi

if [ -z "$(docker images -q ${NF_IMAGE}:${NF_VERSION})" ]; then
    docker pull ${NF_IMAGE}:${NF_VERSION}
fi

nfcli=$(mktemp)
docker run --rm ${NF_IMAGE}:${NF_VERSION} nfcli >"${nfcli}"
NF_IMAGE=${NF_IMAGE} NF_VERSION=${NF_VERSION} sh "${nfcli}" $* || (rm "${nfcli}" ; exit 1)
rm "${nfcli}"
