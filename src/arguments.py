import pathlib
import os
import argparse
from argparse import Namespace


def is_directory(path: str):
    return os.path.exists(path)


def is_file(path: str):
    return os.path.isfile(path)


def parse_arguments() -> Namespace:
    """
    Parsing command line arguments

    :return: Namespace instance for further processing
    """
    # TODO: Add default string parameters to arguments - to prevent problem when argument is None
    parser = argparse.ArgumentParser(description='Choosing video or audio to download')
    parser.add_argument('--url', '-u', required=False, default=False, action='store', type=str,
                        help='Specify video URL', dest='url')
    parser.add_argument('--file', '-f', required=False, default=False, action='store', type=str,
                        help='Specify file path with URLs to load', dest='file')
    parser.add_argument('--video', default=False, required=False, action='store_true', help='Download audio only',
                        dest='video')
    parser.add_argument('--audio', default=False, required=False, action='store_true', help='Download audio only',
                        dest='audio')
    parser.add_argument('--resolution', '-r', required=False, action='store', type=str,
                        help='Specify video resolution (1080p)', dest='resolution')
    parser.add_argument('--directory', '-d', help='Download directory', action='store', required=False,
                        dest='directory', type=str)
    parser.add_argument('--output', '-o', help='Output filename', required=False, action='store', type=str,
                        dest='output')
    return parser.parse_args()


class Arguments:

    def __init__(self):
        self.directory: str = ""
        self.output: str = ""
        self.resolution: str = ""
        self.audio_only: str = ""
        self.video_only: str = ""
        self.url: list = []

    def check_arguments(self):
        args: Namespace = parse_arguments()
        self.video_only = args.video
        self.audio_only = args.audio

        if len(args.resolution) > 1:
            self.resolution = args.resolution

        if is_directory(args.directory):
            self.directory = args.directory

        if len(args.output) > 1:
            self.output = args.output

        if args.directory is not None and is_file(args.file):
            self.read_file(args.file)
        elif len(args.url) > 1:
            self.url.append(args.url)
        else:
            raise ValueError("Single URL or a file with multiple URLs have to be specified")

    def read_file(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.url.append(line.strip())

    def __str__(self):
        return f'Directory: {self.directory}, output: {self.output}, resolution: {self.resolution}, ' \
               f'audio only: {self.audio_only}, video only: {self.video_only}, URL(s): {self.url}'