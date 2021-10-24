#!/usr/bin/env bash
docker exec -it $(grep -oP "IMG_NAME = \K\w+" Makefile)-cntr bash