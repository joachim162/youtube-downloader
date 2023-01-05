from typing import List, Any
from file import File
from arguments import Arguments
from pytube import YouTube, Stream, StreamQuery
from converter import concat
import os


def get_res(file: File) -> list:
    """
    Return a list of available resolutions
    :param file: Current downloading file
    :type file: File
    :return: List of available resolutions
    :rtype: list
    """
    resolutions: list = []
    for res in file.yt.streams.filter(only_video=True):
        resolutions.append(res.resolution)
    return list(dict.fromkeys(resolutions))  # Removing duplicates


def rm_tmp_files(video_path: list, audio_path: list):
    """
    Remove temporary video and audio files
    """
    # TODO: Implement method
    # TODO: Make sure to recognize tmp file over the final
    # One way to do so is to rename the file during concat method
    for video, audio in zip(video_path, audio_path):
        os.remove(video)
        os.remove(audio)


class Downloader:
    """
    Represents a class of a download manager
    """
    index = 0  # Index of current downloading file
    index_video = 0  # Index of current downloading video
    index_audio = 0  # Index of current downloading audio

    def __init__(self, args: Arguments):
        """
        Initialize Downloader class
        :param args: Arguments from CLI
        :type args: Arguments
        """
        self.args: Arguments = args
        self.files: list = self.generate_files()

    def generate_files(self) -> list:
        """
        Create instances of File class and append them to {self.files} list

        :return: List of URLs
        :rtype: list
        """
        tmp_list: list = []
        for url in self.args.url:
            tmp_list.append(File(url, self.args.video_only, self.args.audio_only))
        return tmp_list

    # TODO: Create an algorithm that handles batch downloads
    def download(self) -> None:
        """
        Check
        """
        # TODO: Add a reaction to situation where arguments for video and audio only are both True
        if self.args.video_only:
            self.download_video()
        elif self.args.audio_only:
            self.download_audio()
        else:
            self.download_file()

    def download_video(self) -> list[str]:
        """
        Download video only
        :return: Paths to saved video files
        :rtype: list[str]
        """
        # Absolute paths to saved video files
        paths: list = []
        # TODO: Test if it's necessary to format filename
        for file in self.files:
            video = file.yt.streams.filter(only_video=True)
            if self.args.resolution != "":
                video = self.check_resolution(file.yt).first()
            else:
                # Getting video in the highest resolution (in pytube case, it's 720p for whatever reason)
                video = file.yt.streams.get_high_resolution()
            self.show_info(file, video.filesize_mb, video=True)
            paths.append(video.download(output_path=self.args.directory, filename=file.filename))
            self.index_video += 1
        return paths

    def download_audio(self) -> list[str]:
        """
        Download audio only
        :return: Paths to saved video files
        :rtype: list[str]
        """
        # Absolute paths to saved audio files
        paths: list = []
        for file in self.files:
            audio = file.yt.streams.filter(only_audio=True)
            audio = audio.get_audio_only()
            audio = file.yt.streams.get_by_itag(audio.itag)
            # file.filename = format_name(file, audio=True)
            self.show_info(file, audio.filesize_mb, audio=True)
            paths.append(audio.download(output_path=self.args.directory, filename=file.filename))
            # audio.download(output_path=self.args.directory)
            self.index_audio += 1
        return paths

    def download_file(self) -> None:
        """
        Download video with audio
        """
        # TODO: Implement method
        # TODO: Test method
        # TODO: Fix issue with filename and title, if custom filename is provided it has to be handled properly
        for file in self.files:
            if self.args.resolution != "" and int(self.args.resolution[:-1]) > 720:
                paths_video = self.download_video()
                paths_audio = self.download_audio()
                # This is problem, a concat method needs valid video and audio path
                # concat(paths_video, paths_audio)
                rm_tmp_files(paths_video, paths_audio)

            else:
                down_file = file.yt.streams.get_high_resolution()
                self.show_info(file, down_file.filesize_mb)
                down_file.download(output_path=self.args.directory, filename=file.filename)

    def check_resolution(self, file: File) -> StreamQuery:
        """
        Check if file is available in prompted resolution.
        If not, user can choose from available resolutions.
        :param file: Currently downloading file
        :type file: File
        :return: Query with available resolutions
        :rtype: StreamQuery
        """
        available_resolutions = file.yt.streams.filter(res=self.args.resolution)
        if len(available_resolutions) > 0:
            return available_resolutions
        else:
            print(f'Unfortunately, {file.title} with resolution {self.args.resolution} is not available')
            print('Here is a list with resolutions that are available:')
            print(get_res(file=file))
            self.args.resolution = int(input('Please, choose a resolution from the list above: '))
            self.check_resolution(file)

    def show_info(self, file: File, filesize_mb: float, video: bool = False, audio: bool = False) -> None:
        """
        Print info about download progress
        :param file: Current downloading file
        :type file: File
        :param filesize_mb: File size
        :type filesize_mb: float
        :param video: Video flag
        :type video: bool
        :param audio: Audio flag
        :type audio: bool
        """
        if video:
            print(f'[INFO] Downloading video "{file.filename}", '
                  f'with size of {filesize_mb} in MB, to {self.args.directory}')
        elif audio:
            print(f'[INFO] Downloading audio "{file.filename}", '
                  f'with size of {filesize_mb} in MB, to {self.args.directory}')
