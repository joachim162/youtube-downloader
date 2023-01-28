# YouTube CLI app

Easy CLI tool for downloading content from YouTube. Supports downloading video or audio only
content and downloading videos in full quality (not limited to 720p).

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Installing

The easiest way to use the script is to create a single executable file, that can
be used acrossed platforms, using Pyinstaller tool. There is a script in scripts directory that
will auto generate the executable. Should be working on Linux and Windows, but I didn't
have the option to try it out on macOS.

## Built With

The script itself use Python only. Downloading content from YouTube is handled
by [pytube](https://pypi.org/project/pytube/). When downloading video with resolution higer than
720p, audio and video files have to be downloaded separately and subsequently merged together using [moviepy](https://pypi.org/project/moviepy). Unfortunately this approach is quite slow, consider using CPU only. I am already finding a way to take advantage of GPU acceleration that should speed up the process.
## Authors

  - **Jáchym Holeček** - *Author* -
    [joachim162](https://github.com/joachim162)

  - **Billie Thompson** - *Provided README Template* -
    [PurpleBooth](https://github.com/PurpleBooth)