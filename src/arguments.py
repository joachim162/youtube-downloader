import pathlib
import os
import argparse
from argparse import Namespace


def parse_arguments() -> Namespace:
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
                        dest='directory', type=str)
    parser.add_argument('--output', '-o', help='Output filename', required=False, action='store', type=str,
                        dest='output')
    return parser.parse_args()


class Arguments:

    def __init__(self):
        self.output = None
        self.resolution = None
        self.audio_only = None
        self.video_only = None
        self.url: list = []

    def check_arguments(self):
        # TODO: Process arguments and save them to class variables
        args: Namespace = parse_arguments()


    def read_file(self, file):
        with open(file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                self.url.append(line.strip())
