#!/bin/sh

origin=$(pwd)
cd $(dirname $(realpath $0)) && make docker && cd $origin
docker run --rm -v $(pwd):/project nf $*
