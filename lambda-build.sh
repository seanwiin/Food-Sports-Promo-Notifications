#!/bin/bash

echo "Building .zip for Lambda"

echo "Removing any previous build(s)/artifacts"

pip install -r requirements.txt -t build/
cp baseball.py build/

echo "Zipping contents"
cd ./build
zip -r lambda_handler.zip ./*