#!/bin/bash

# Bash script to build a single executable to run the app
cd ..
pyinstaller --noconfirm --onefile --console --name "yt-downloader" --add-binary "$(readlink -f src/file.py):." --add-binary "$(readlink -f src/downloader.py):." --add-binary "$(readlink -f src/arguments.py):." --hidden-import "pytube" "$(readlink -f src/__init__.py)"

rm -rf build/
mv dist/yt-downloader . && rm -rf dist
echo Executable has been created successfully in $(readlink -f ./yt-downloader)