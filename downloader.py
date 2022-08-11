from pytube import YouTube, Stream, StreamQuery
from converter import concat
import os


def format_title_helper(title: str):
    """
    Remove unwanted characters from title

    :param title: title to format
    :return: formatted title
    """
    title = title.strip()
    title = title.replace('"', '')
    title = title.replace(' ', '_')
    title = title.replace('/', '')
    title = title.replace("'", "")
    return title


class Downloader:
    """
    Class represents a downloader
    """
    def __init__(self, url: str, download_path: str = '.', resolution: str = None, video_only: bool = False,
                 audio_only: bool = False):
        """
        Initialize Downloader class

        :param url: Video URL
        :param download_path: Download path
        :param resolution: Video resolution
        :param video_only: If true, only video will be downloaded
        :param audio_only: If true, only audio will be downloaded
        """
        self.url = url
        self.download_path = download_path
        self.resolution = resolution
        self.video_only = video_only
        self.audio_only = audio_only

        self.yt = YouTube(self.url)
        self.title = self.yt.title
        self.video_title = ''
        self.audio_title = ''

    def download(self) -> None:
        """
        Decide if user wants to download file with video and audio, or just video or just audio

        :return: None
        """
        if self.video_only is False and self.audio_only is False:
            self.download_file()
        elif self.video_only:
            self.download_video()
        else:
            self.download_audio()

    def download_video(self) -> None:
        """
        Download video only

        :return: None
        """
        file = self.yt.streams.filter(only_video=True)
        if self.resolution is not None:
            file = self.check_resolution().first()
        else:
            # Getting video in the highest resolution (720p in this case)
            file = self.yt.streams.get_highest_resolution()
        # show_info(file, f'{file.title}.mp4')  # Printing additional information about video
        self.format_title(video=True)
        file.download(output_path=self.download_path, filename=self.video_title)  # Downloading video

    def download_audio(self) -> None:
        """
        Download audio only

        :return: None
        """
        file = self.yt.streams.filter(only_audio=True)
        file = file.get_audio_only()
        file = self.yt.streams.get_by_itag(file.itag)
        self.format_title(audio=True)
        self.show_info(file.filesize, audio=True)
        file.download(output_path=self.download_path, filename=self.audio_title)

    def download_file(self) -> None:
        """
        Download both video and audio

        :return: None
        """
        if self.resolution is not None:
            resolution: int = int(self.resolution[:-1])  # Removing 'p' from variable (1080p -> 1080p)
            if resolution > 720:
                self.download_video()
                self.download_audio()
                video_path = f'{self.download_path}/{self.video_title}'
                audio_path = f'{self.download_path}/{self.audio_title}'
                print(f'[INFO] Merging video and audio files...')
                concat(video_path, audio_path, self.video_title, self.download_path)
                print(f'[INFO] Removing temporary files...')
                self.rm_tmp_files()
        else:
            file = self.yt.streams.get_highest_resolution()
            self.show_info(file.filesize, video=True)
            file.download(output_path=self.download_path)

    def show_info(self, file_size: float, video: bool = False, audio: bool = False) -> None:
        """
        Print info about download

        :param file_size: File size in bytes
        :param video: True if video
        :param audio:True if audio
        :return: None
        """
        file_size: int = round(file_size / 1024 ** 2, 2)  # Formatting file size to MB and rounding to 2 places
        if video:
            print(f'[INFO] Downloading video "{self.video_title}", '
                  f'with size of {file_size} in MB, to {self.download_path}')
        elif audio:
            print(f'[INFO] Downloading audio "{self.audio_title}", '
                  f'with size of {file_size} in MB, to {self.download_path}')

    def check_resolution(self) -> StreamQuery:
        """
        Return media streams with resolution specified from command line arguments

        :return: StreamQuery instance with specific media streams
        """
        file = self.yt.streams.filter(res=self.resolution)
        if len(file) > 0:
            return file
        else:
            print(f'Video with resolution {self.resolution} is not available')
            print('Here is a list with resolutions that are available:')
            print(self.get_res())
            self.resolution = input('Please, choose a resolution from list above: ')
            self.check_resolution()

    def get_res(self) -> list:
        """
        Return a list of available resolutions

        :return: list with available resolutions
        """
        resolutions: list = []
        for res in self.yt.streams.filter(only_video=True):
            resolutions.append(res.resolution)
        return list(dict.fromkeys(resolutions))  # Removing duplicates

    def format_title(self, video: bool = False, audio: bool = False) -> None:
        """
        Formatting title

        :param video: flag for video
        :param audio: flag for audio
        :return: None
        """
        title = self.title
        if video:
            title = format_title_helper(title)
            if '.mp4' not in title:
                title += '.mp4'
                self.video_title = title
                print(f'video title: {self.video_title}')
        elif audio:
            title = format_title_helper(title)
            if '.mp4' in title:
                title = title[:-3]  # Removing .mp4 from audio file
                title += '.mp3'
                self.audio_title = title
            elif '.mp3' not in title:
                title += '.mp3'
                self.audio_title = title

    def rm_tmp_files(self) -> None:
        """
        Remove temporary video and audio files

        :return: None
        """
        os.remove(f'{self.download_path}/{self.video_title}')
        os.remove(f'{self.download_path}/{self.audio_title}')
