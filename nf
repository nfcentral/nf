#!/bin/sh

command=$1
shift

if [ "${command}" = "generate" ]; then
    docker run --rm -v $(pwd):/project theiced/nf generate $*
else
    sh .nf/nf-${command} $*
fi
