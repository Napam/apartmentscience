#!/usr/bin/env bash
docker exec -it $(rg -oP "IMG_NAME = \K\w+" Makefile)-cntr bash
