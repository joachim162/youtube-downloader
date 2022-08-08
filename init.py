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
    parser.add_argument('--directory', '-d', help='Download directory', action='store', required=False, dest='directory')
    args = parser.parse_args()
    return args


def check_parsing(args=args_parsing()) -> Downloader:
    """
    Check parsing and set parameters to Downloader

    :param args: Command line arguments
    :return: New Downloader instance with parameters from arguments
    """
    downloader = Downloader(url=args.url)
    download_path = os.getcwd()
    if is_dir(args.directory):
        download_path = args.directory
    if args.resolution is not None:
        downloader = Downloader(url=args.url, download_path=download_path, resolution=args.resolution)

    downloader = Downloader(url=args.url, download_path=download_path, resolution=args.resolution,
                            video_only=args.video,
                            audio_only=args.audio)
    return downloader


if __name__ == "__main__":
    check_parsing()
