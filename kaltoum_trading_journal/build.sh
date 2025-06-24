#!/bin/bash

while getopts t: flag
do
    case "${flag}" in
        t) TAG=${OPTARG};;
    esac
done

if [ -z "$TAG" ]; then
  echo "Usage: ./build.sh -t <tag>"
  exit 1
fi

docker build -t kaltoum_trading_journal:$TAG ./trading_app
