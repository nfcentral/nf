#!/bin/sh

origin=$(pwd)
cd $(dirname $(realpath $0)) && docker build -t nf . && cd $origin
docker run --rm -v $(pwd):/project nf $*
