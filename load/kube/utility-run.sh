#!/bin/bash

pip install awscli

while true; do
    for file in $(ls /output); do
        bash /utilities/parse.sh /output/$file || true
    done
    sleep 120
done
