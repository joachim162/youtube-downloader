
# PowerShell script to build a single executable to run the app
Set-Location ..
Set-Location src

pyinstaller --noconfirm --onefile --console --name "yt-downloader" --add-binary (Get-Item -Path '.\file.py').FullName+":." --add-binary (Get-Item -Path '.\downloader.py').FullName+":." --add-binary (Get-Item -Path '.\arguments.py').FullName+":." --hidden-import "pytube" --hidden-import "moviepy.editor" (Get-Item -Path '.\__init__.py').FullName
