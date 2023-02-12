import os
import argparse
import sys
from argparse import Namespace
from urllib.parse import urlparse
from pytube import Playlist


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

def is_playlist(url: str) -> bool:
    """
    Check if URL is a playlist
    :param url: Potential playlist
    :type url: str
    :return: True if URL is a playlist, False otherwise
    """
    p = Playlist(url)
    try:
        return len(p) > 0
    except:
        # print('Entered URL is not a playlist')
        return False


def parse_arguments() -> Namespace:
    """
    Parsing command line arguments
    :return: CLI arguments
    :rtype: Namespace
    """
    parser = argparse.ArgumentParser(description='Available options:')
    parser.add_argument('--url', '-u', required=False, default='', action='store', type=str,
                        help='Specify video URL', dest='url')
    parser.add_argument('--file', '-f', required=False, default='', action='store', type=str,
                        help='Specify file path with URLs to load', dest='file')
    parser.add_argument('--video', default=False, required=False, action='store_true', help='Download audio only',
                        dest='video')
    parser.add_argument('--audio', default=False, required=False, action='store_true', help='Download audio only',
                        dest='audio')
    parser.add_argument('--resolution', '-r', required=False, action='store', type=str,
                        help='Specify video resolution in "1080p" format', dest='resolution', default="")
    parser.add_argument('--directory', '-d', help='Download directory', action='store', required=False,
                        dest='directory', type=str, default=os.getcwd())
    return parser.parse_args()


def read_file(filepath: str) -> list:
    """
    Read URLS from file, append them to {tmp_list} list and return it
    :param filepath: Absolute path to file with URLs
    :type filepath: str
    :return: List with URLs
    """
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

    # List with valid YT resolutions
    res_list: list[str] = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]

    def __init__(self):
        self._directory: str = ""
        # self._output: str = ""
        self._resolution: str = ""
        self._audio_only: str = ""
        self._video_only: str = ""
        self._url: list = []
        self.check_arguments()

    def __str__(self):
        return f'Directory: {self.directory}, resolution: {self.resolution}, ' \
               f'audio only: {self.audio_only}, video only: {self.video_only}, URL(s): {self.url}'

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, value: str):
        if is_directory(value):
            self._directory = value
        else:
            sys.exit(f"Directory: '{value}' does not exist.")

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value: str):
        """
        Check format of prompted resolution and its presence in {res_list}
        :param value: Resolution value from CLI arguments
        :type value: str
        """
        if value != "" and value[-1] == 'p' and value in self.res_list:
            self._resolution = value

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
    def url(self, value: list) -> None:
        """
        Check {url} argument and test if it's a single URL or a file path
        :param value: URL argument
        :type value: str
        """
        try:
            url_arg, file_arg = value
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        
        tmp_list = []
        if file_arg != "" and is_file(file_arg):
            tmp_list = read_file(file_arg)
        elif is_url(url_arg):
            tmp_list.append(url_arg)
            if is_playlist(url_arg):
                p = Playlist(url_arg)
                tmp_list = list(p.video_urls)
        else:
            raise ValueError("Single URL or file path with multiple URLs have to be specified")
        self._url = tmp_list

    def check_arguments(self):
        """
        Checking CLI arguments
        """

        # Getting CLI arguments
        args: Namespace = parse_arguments()

        self.directory = args.directory
        self.resolution = args.resolution
        self.audio_only = args.audio
        self.video_only = args.video
        
        # Exit program if required arguments are not specified
        try:
            self.url = args.url, args.file
        except ValueError:
            print("Missing --url of --file argument")
            sys.exit()

