import pathlib
import os
import argparse
from argparse import Namespace
from downloader import Downloader


def is_dir(path: str) -> bool:
    """
    Check if directory from argument exists

    :param path: path to check
    :return: True if directory exists, False if otherwise
    """
    return pathlib.Path(path).absolute().is_dir()


def args_parsing() -> Namespace:
    """
    Parsing command line arguments

    :return: Namespace instance for further processing
    """
    parser = argparse.ArgumentParser(description='Choosing video or audio to download')
    parser.add_argument('--url', '-u', required=True, default=False, action='store', type=str,
                        help='Specify video URL', dest='url')
    parser.add_argument('--video', default=False, required=False, action='store_true', help='Download audio only',
                        dest='video')
    parser.add_argument('--audio', default=False, required=False, action='store_true', help='Download audio only',
                        dest='audio')
    parser.add_argument('--resolution', '-r', required=False, action='store', type=str,
                        help='Specify video resolution (1080p)', dest='resolution')
    parser.add_argument('--directory', '-d', help='Download directory', action='store', required=False,
                        dest='directory')
    parser.add_argument('--output', '-o', help='Output filename', required=False, action='store', type=str,
                        dest='output')
    args = parser.parse_args()
    return args


def check_parsing(args=args_parsing()) -> Downloader:
    """
    Check parsing and set parameters to Downloader

    :param args: Parsed command line arguments
    :return: New Downloader instance with parameters from arguments
    """
    download_path = os.getcwd()
    resolution = None
    if is_dir(args.directory):
        download_path = args.directory
    if args.resolution is not None:
        resolution = args.resolution

    return Downloader(url=args.url,
                      download_path=download_path,
                      resolution=resolution,
                      video_only=args.video,
                      audio_only=args.audio)


if __name__ == "__main__":
    downloader = check_parsing()  # Downloader instance with video information
    downloader.download()  # Starting downloading
