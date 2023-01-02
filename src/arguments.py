import os
import argparse
from argparse import Namespace
from urllib.parse import urlparse

res_list: list = [144, 240, 360, 480, 720, 1080, 1440, 2160]  # List with valid YT resolutions


def is_directory(path: str):
    return os.path.exists(path)


def is_file(path: str):
    return os.path.isfile(path)


def is_url(string):
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError("Prompted URL is not valid"):
        return False


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
    parser.add_argument('--resolution', '-r', required=False, action='store', type=str,
                        help='Specify video resolution in integer (1080)', dest='resolution', default=0)
    parser.add_argument('--directory', '-d', help='Download directory', action='store', required=False,
                        dest='directory', type=str, default=os.getcwd())
    parser.add_argument('--output', '-o', help='Output filename', required=False, action='store', type=str,
                        dest='output', default='.')
    return parser.parse_args()


def read_file(filepath: str) -> list:
    """
    Read URLS from file, append them to {url} list and return it
    :param filepath: Absolute path to file with URLs
    :type filepath: str
    """
    # TODO: Fix docstring
    tmp_list = []
    with open(filepath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            tmp_list.append(line.strip())
    return tmp_list


class Arguments:
    """
    Represents a class for CLI arguments
    """

    def __init__(self):
        self._directory: str = ""
        self._output: str = ""
        self._resolution: str = ""
        self._audio_only: str = ""
        self._video_only: str = ""
        self._url: list = []
        self.check_arguments()

    def __str__(self):
        return f'Directory: {self.directory}, output: {self.output}, resolution: {self.resolution}, ' \
               f'audio only: {self.audio_only}, video only: {self.video_only}, URL(s): {self.url}'

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value: str):
        self._directory = value

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value: str):
        self._output = value

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value: str):
        if value[-1] == 'p' and value in res_list:
            self._resolution = value
        raise argparse.ArgumentTypeError(f'{value} is not a valid resolution')

    @property
    def video_only(self):
        return self._video_only

    @video_only.setter
    def video_only(self, value: bool):
        self._video_only = value

    @property
    def audio_only(self):
        return self._audio_only

    @audio_only.setter
    def audio_only(self, value: bool):
        self._audio_only = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value: str):
        tmp_list = []
        if value != "" and is_file(value):
            tmp_list = read_file(value)
        elif is_url(value):
            tmp_list.append(value)
        else:
            raise ValueError("Single URL or a file path with multiple URLs have to be specified")
        self._url = tmp_list

    def check_arguments(self):
        """
        Checking CLI arguments
        """
        # TODO: Implement getters and setters for this section and move the if statement to them
        args: Namespace = parse_arguments()

        self.directory = args.directory
        self.output = args.output
        self.resolution = args.resolution
        self.audio_only = args.audio
        self.video_only = args.video
        self.url = args.url
