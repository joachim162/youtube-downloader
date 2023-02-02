# YouTube CLI app

Easy CLI tool for downloading content from YouTube. Supports downloading video or audio only
content and downloading videos in full quality (not limited to 720p).

## Getting Started

These instructions will give you an idea how to use this tool. The most important argument is *--url*. URL has to be specified. Then you can choose to download it both audio and video or separately. With *--file* you can specify a text file that contains list of URLs so that you can download videos in batch. You can print the usage shown below using *--help*.
```
usage: __init__.py [-h] [--url URL] [--file FILE] [--video] [--audio] [--resolution RESOLUTION] [--directory DIRECTORY]

Available options:

options:
  -h, --help            show this help message and exit
  --url URL, -u URL     Specify video URL
  --file FILE, -f FILE  Specify file path with URLs to load
  --video               Download audio only
  --audio               Download audio only
  --resolution RESOLUTION, -r RESOLUTION
                        Specify video resolution in "1080p" format
  --directory DIRECTORY, -d DIRECTORY
                        Download directory
```

### Installing

The easiest way to use the script is to create a single executable file, that can
be used acrossed platforms, using Pyinstaller tool. There is a script in *scripts* directory that
will auto generate the executable. It should be working both on Linux and Windows, but I didn't
have the option to try it out on macOS. 
With the executable, you can copy it to PATH environment and use it directly from command line.

## Built With

The script itself use Python only. Downloading content from YouTube is handled
by [pytube](https://pypi.org/project/pytube/). When downloading video with resolution higer than
720p, audio and video files have to be downloaded separately and subsequently merged together using [moviepy](https://pypi.org/project/moviepy). Unfortunately this approach is quite slow, considered using CPU only. I am already finding a way to take advantage of GPU acceleration that should speed up the process.
## Authors

  - **Jáchym Holeček** - *Author* -
    [joachim162](https://github.com/joachim162)

  - **Billie Thompson** - *Provided README Template* -
    [PurpleBooth](https://github.com/PurpleBooth)