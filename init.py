import sys
import os
import argparse
from argparse import Namespace
from downloader import Downloader


def args_parsing() -> Namespace:
    parser = argparse.ArgumentParser(description='Choosing video or audio to download')
    parser.add_argument('--url', '-u', required=True, default=False, action='store', type=str,
                        help='Specify video URL')
    parser.add_argument('--video', default=False, required=False, action='store_true', help='Download audio only')
    parser.add_argument('--audio', default=False, required=False, action='store_true', help='Download audio only')
    parser.add_argument('--resolution', '-r', required=False, action='store', type=str, help='Specify video '
                                                                                             'resolution (1080p)')
    parser.add_argument('dir', nargs='?', default='.', help='Directory for downloaded file')
    args = parser.parse_args()
    return args


def check_parsing(args=args_parsing()) -> Downloader:
    """
    Check parsing and set parameters to Downloader
    :param args: Command line arguments
    :return: New Downloader instance with parameters from arguments
    """
    downloader = Downloader(url=args.url)
    if os.path.isdir(sys.argv[-1]):
        downloader = Downloader(url=args.url, download_path=sys.argv[-1])
    if args.resolution is not None:
        downloader = Downloader(url=args.url, download_path=sys.argv[-1], resolution=args.resolution)

    downloader = Downloader(url=args.url, download_path=sys.argv[-1], resolution=args.resolution,
                            video_only=args.video,
                            audio_only=args.audio)
    return downloader


if __name__ == "__main__":
    check_parsing()
