
# PowerShell script to build a single executable to run the app
Set-Location ..
Set-Location src

pyinstaller --noconfirm --onefile --console --name "yt-downloader" --add-binary "file.py;." --add-binary "downloader.py;." --add-binary "arguments.py;." --hidden-import "pytube" --hidden-import "moviepy.editor" "__init__.py"