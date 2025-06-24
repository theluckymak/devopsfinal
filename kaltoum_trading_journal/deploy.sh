#!/bin/bash

TAG="latest"

while getopts "t:" opt; do
  case $opt in
    t)
      TAG=$OPTARG
      ;;
    *)
      echo "Usage: $0 -t <tag>"
      exit 1
      ;;
  esac
done

echo "Building image with tag: $TAG"
docker compose build --build-arg TAG=$TAG
docker compose up -d

