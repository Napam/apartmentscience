#!/usr/bin/env bash
containerEngine=${CONTAINER_ENGINE:-docker}
${containerEngine} exec -it $(rg -oP "img_name = \K\w+" Makefile)-cntr bash
