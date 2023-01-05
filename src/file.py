from pytube import YouTube
from arguments import Arguments


def help_format_name(filename: str) -> str:
    """
    Remove illegal characters from filename (Windows, macOS, Linux)
    :param filename: File name to format
    :type filename: str
    :return: Formatted file name
    :rtype: str
    """
    # TODO: Test
    filename = filename.strip()
    filename = filename.replace('"', '')
    filename = filename.replace(' ', '_')
    filename = filename.replace('/', '')
    filename = filename.replace("'", "")
    filename = filename.replace("|", "")
    filename = filename.replace(":", "")
    filename = filename.replace("*", "")
    filename = filename.replace("?", "")
    filename = filename.replace("<", "")
    filename = filename.replace(">", "")
    return filename


class File:
    """
    Represents a single file to download
    """
    def __init__(self, url: str, video: bool, audio: bool):
        """
        Initialize File class
        :param url: URL of YT video
        :type url: str
        """
        self._url: str = url
        self._yt: YouTube = YouTube(self._url)
        self._title: str = self._yt.title
        self._video: bool = video
        self._audio: bool = audio
        self._filename: str = self.format_filename()

    @property
    def url(self):
        return self._url

    @property
    def yt(self):
        return self._yt

    @property
    def title(self):
        return self._title

    @property
    def video(self):
        return self._video

    @property
    def audio(self):
        return self._audio

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    def format_filename(self) -> str:
        """
        Format filename
        :return: New filename
        :rtype: str
        """
        # TODO: Test the method
        filename = self.title
        if self.video:
            new_filename = help_format_name(filename)
            if '.mp4' not in new_filename:
                new_filename += '.mp4'
                return new_filename
        elif self.audio:
            new_filename = help_format_name(filename)
            if '.mp4' in new_filename:
                new_filename = new_filename[:-3]  # Removing .mp4 from audio file
                new_filename += '.mp3'
            elif '.mp3' not in new_filename:
                new_filename += '.mp3'
            return new_filename
