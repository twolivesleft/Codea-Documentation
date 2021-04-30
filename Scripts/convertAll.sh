#!/bin/bash

for file in ../*.yaml; do
    python3 convertToHtml.py "$file" > ../Web/"`basename $file .yaml`.html"
done
