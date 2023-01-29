#!/bin/bash

# Bash script to build a single executable to run the app
cd .. && cd src/
pyinstaller --noconfirm --onefile --console --name0 "yt-downloader" --add-binary "$(readlink -f file.py):." --add-binary "$(readlink -f downloader.py):." --add-binary "$(readlink -f arguments.py):." --hidden-import "pytube" --hidden-import "moviepy.editor" "$(readlink -f __init__.py)"
