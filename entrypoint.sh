#!/bin/bash
set -e

if [[ $1 = "base" ]];
  then
    shift
fi

exec $@
