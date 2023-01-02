import os
import argparse
from argparse import Namespace

res_list: list = [144, 240, 360, 480, 720, 1080, 1440, 2160]  # List with valid YT resolutions


def is_directory(path: str):
    return os.path.exists(path)


def is_file(path: str):
    return os.path.isfile(path)


def is_resolution(resolution: str) -> str:
    """
    Check if resolution from argument is a valid YT resolution
    :param resolution:
    :type resolution:
    :return:
    :rtype:
    """
    # TODO: Test the functionality
    # TODO: Change the list of resolutions to str, pytube accepts resolution in "1080p" format
    value = resolution
    if value[-1] == 'p' and value in res_list:
        return value
    raise argparse.ArgumentTypeError(f'{resolution} is not a valid resolution')


def parse_arguments() -> Namespace:
    """
    Parsing command line arguments
    :return: CLI arguments
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description='Choosing video or audio to download')
    parser.add_argument('--url', '-u', required=False, default="", action='store', type=str,
                        help='Specify video URL', dest='url')
    parser.add_argument('--file', '-f', required=False, default='', action='store', type=str,
                        help='Specify file path with URLs to load', dest='file')
    parser.add_argument('--video', default=False, required=False, action='store_true', help='Download audio only',
                        dest='video')
    parser.add_argument('--audio', default=False, required=False, action='store_true', help='Download audio only',
                        dest='audio')
    parser.add_argument('--resolution', '-r', required=False, action='store', type=is_resolution,
                        help='Specify video resolution in integer (1080)', dest='resolution', default=0)
    parser.add_argument('--directory', '-d', help='Download directory', action='store', required=False,
                        dest='directory', type=str, default=os.getcwd())
    parser.add_argument('--output', '-o', help='Output filename', required=False, action='store', type=str,
                        dest='output', default='.')
    return parser.parse_args()


class Arguments:
    """
    Represents a class for CLI arguments
    """
    def __init__(self):
        self.directory: str = ""
        self.output: str = ""
        self.resolution: str = ""
        self.audio_only: str = ""
        self.video_only: str = ""
        self.url: list = []
        self.check_arguments()

    def __str__(self):
        return f'Directory: {self.directory}, output: {self.output}, resolution: {self.resolution}, ' \
               f'audio only: {self.audio_only}, video only: {self.video_only}, URL(s): {self.url}'

    def check_arguments(self):
        """
        Checking CLI arguments
        """
        args: Namespace = parse_arguments()
        self.video_only = args.video
        self.audio_only = args.audio

        if args.resolution != 0:
            self.resolution = args.resolution

        if is_directory(args.directory):
            self.directory = args.directory

        if len(args.output) > 1:
            self.output = args.output

        if args.file != "" and is_file(args.file):
            self.read_file(args.file)
        elif len(args.url) > 1:
            self.url.append(args.url)
        else:
            raise ValueError("Single URL or a file path with multiple URLs have to be specified")

    def read_file(self, filepath: str) -> None:
        """
        Read URLS from file and append them to {url} list
        :param filepath: Absolute path to file with URLs
        :type filepath: str
        """
        with open(filepath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.url.append(line.strip())
