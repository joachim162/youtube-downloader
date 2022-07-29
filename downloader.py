from pytube import YouTube, Stream, StreamQuery
from converter import concat


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
        self.download()

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
            file = self.yt.streams.get_highest_resolution()  # Getting video in the highest resolution (720p in this case)
        # show_info(file, f'{file.title}.mp4')  # Printing additional information about video
        file.download(output_path=self.download_path)  # Downloading video

    def download_audio(self) -> None:
        """
        Download audio only
        :return: None
        """
        file = self.yt.streams.filter(only_audio=True)
        file = file.get_audio_only()
        file = self.yt.streams.get_by_itag(file.itag)
        filename = file.title[:-4]  # Removing last 4 chars, audio file has from unknown reason .mp4 suffix
        filename += '.mp3'
        # show_info(file, filename)
        file.download(output_path=self.download_path, filename=filename)

    def download_file(self) -> None:
        """
        Download both video and audio
        :return: None
        """
        if self.resolution is not None:
            # TODO: Fix this
            resolution: int = int(self.resolution[:-1])  # Removing 'p' from variable (1080p -> 1080p)
            if resolution > 720:
                file_name = self.yt.title
                video_path = f'{self.download_path}/{file_name}.mp4'
                audio_path = f'{self.download_path}/{file_name}.mp3'
                print(video_path)
                print(audio_path)
                self.download_video()
                self.download_audio()
                concat(video_path, audio_path, self.download_path)
        else:
            file = self.yt.streams.get_highest_resolution()
            file.download(output_path=self.download_path)

    """
    def show_info(self):
        file_size: int = round(self.yt.filesize / 1024 ** 2, 2)  # File size in MB
        print(f'[INFO] Downloading "{yt.title}", with size of {file_size} MB, in {filename[-3:]} format')
    """
    
    def check_resolution(self) -> StreamQuery:
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
        resolutions = list(dict.fromkeys(resolutions))  # Removing duplicates
        return resolutions
