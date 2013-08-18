#!/bin/bash

for file in ../*.yaml; do
    python html.py "$file" > ../Web/"`basename $file .yaml`.html"
done
