#!/bin/zsh
docker rm --force notify-sunset
docker run --name notify-sunset notify-sunset-image
