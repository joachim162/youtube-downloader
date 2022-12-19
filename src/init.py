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
    return pathlib.Path(str(path)).absolute().is_dir()


def is_file(path: str) -> bool:
    """
    Check if file from argument exists

    :param path: file path to check
    :return: True if file exists, False if otherwise
    """
    return pathlib.Path(str(path)).absolute().is_file()


def read_file(path) -> list:
    """
    Read file with URLs and return them in list

    :param path: file path with URLs
    :return: list filled with URLs
    """
    urls: list = []  # New list
    with open(path, 'r') as reader:
        for line in reader.read().splitlines():
            urls.append(line)
    return urls


def args_parsing() -> Namespace:
    """
    Parsing command line arguments

    :return: Namespace instance for further processing
    """
    parser = argparse.ArgumentParser(description='Choosing video or audio to download')
    parser.add_argument('--url', '-u', required=False, default=False, action='store', type=str,
                        help='Specify video URL', dest='url')
    parser.add_argument('--file', '-f', required=False, default=False, action='store', type=str,
                        help='Specify file path with multiple URLs', dest='file')
    parser.add_argument('--video', default=False, required=False, action='store_true', help='Download audio only',
                        dest='video')
    parser.add_argument('--audio', default=False, required=False, action='store_true', help='Download audio only',
                        dest='audio')
    parser.add_argument('--resolution', '-r', required=False, action='store', type=str,
                        help='Specify video resolution (1080p)', dest='resolution')
    parser.add_argument('--directory', '-d', help='Download directory', action='store', required=False,
                        dest='directory', type=str)
    parser.add_argument('--name', '-n', help='Output filename', required=False, action='store', type=str,
                        dest='name', default=None)
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
    if args.file is not None and is_file(args.file):
        url = read_file(args.file)
        return Downloader(url=url,
                          download_path=download_path,
                          resolution=resolution,
                          video_only=args.video,
                          audio_only=args.audio,
                          filename=args.name)
    else:
        return Downloader(url=args.url,
                          download_path=download_path,
                          resolution=resolution,
                          video_only=args.video,
                          audio_only=args.audio,
                          filename=args.name)


if __name__ == "__main__":
    downloader = check_parsing()  # Downloader instance with video information
    downloader.download()  # Starting downloading
    if downloader.filename is not None:
        downloader.rename_file()
