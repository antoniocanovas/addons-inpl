#!/bin/bash
for file in $(find . -name "*.pyc"); do
    git update-index --assume-unchanged "$file" || echo "No se pudo marcar: $file"
done
