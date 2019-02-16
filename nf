#!/bin/sh

command=$1
shift

case $command in
    new)
        name=$1
        mkdir ${name}
        cat << EOF > ${name}/nf.json
{
  "name": "${name}",
  "template": "starlette",
  "python": "3.7.2",
  "features": []
}
EOF
    ;;
    generate)
        docker run --rm -v $(pwd):/project theiced/nf generate $*
        ;;
    *)
        sh .nf/commands/${command} $*
        ;;
esac
