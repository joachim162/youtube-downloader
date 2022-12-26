from pytube import YouTube


class Video:
    """
    Represents a single video to download
    """
    def __init__(self, url):
        """
        Initialize Video class
        """
        self.url = url
        self.yt = YouTube(self.url)
        self.title = self.yt.title
