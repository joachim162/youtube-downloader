from pytube import YouTube
from arguments import Arguments


class File:
    """
    Represents a single file to download
    """
    def __init__(self, url: str):
        """
        Initialize File class
        :param url: URL of YT video
        :type url: str
        """
        self.url: str = url
        self.yt: YouTube = YouTube(self.url)
        self.title: str = self.yt.title
        self.filename: str = ""
