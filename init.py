import sys
import os
import argparse
from pytube import YouTube


def args_parsing():
    download_dir = ''

    # TODO: Implement parsing arguments
    parser = argparse.ArgumentParser(description='Choosing video or audio to download')
    parser.add_argument('--url', '-u', required=True, default=False, action='store', type=str,
                        help='Specify video URL')
    parser.add_argument('--audio', default=False, action='store_true', help='Download audio only')
    args = parser.parse_args()
    print(type(args))

    if os.path.isdir(sys.argv[-1]):
        download_dir = sys.argv[-1]
    if args.audio:
        download_audio(args.url, download_dir)
        print('download audio')
    if not args.audio:
        download_video(url, download_dir)


def download_video(url: str, download_dir: str):
    # TODO: Implement method for video download
    yt = YouTube(url)
    file = yt.streams.get_highest_resolution()
    print(type(file))
    # file.download(output_path=download_dir, filename_prefix='.mp4')


def download_audio(url: str, download_dir: str):
    # TODO: Implement method
    yt = YouTube(url)
    file = yt.streams.filter(only_audio=True)
    file = file.get_audio_only()
    file = yt.streams.get_by_itag(file.itag)
    file.download(output_path=download_dir, filename_prefix='.mp3')


def show_info(yt: YouTube.streams):
    """
    Prints out file information
    :param yt: YT video instance
    """
    # TODO: Implement method
    file_size = ''
    print(f'[INFO] Downloading file "{yt.title}", with size of {file_size}')


if __name__ == "__main__":
    args_parsing()
