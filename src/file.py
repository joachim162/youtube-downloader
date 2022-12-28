from pytube import YouTube
from arguments import Arguments


class File:
    """
    Represents a single file to download
    """
    def __init__(self, url):
        """
        Initialize Video class
        """
        self.url = url
        self.yt = YouTube(self.url)
        self.title = self.yt.title
