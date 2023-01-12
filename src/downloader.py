from typing import List, Any
from file import File
from arguments import Arguments
from pytube import YouTube, Stream, StreamQuery
import os

# TODO: Make code more readable


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


def concat(video_path: list, audio_path: list) -> None:
    """
    Merge video and audio to one file
    :param video_path: Paths to video files
    :type video_path: list
    :param audio_path: Paths to audio files
    :type audio_path: list
    """
    from moviepy.editor import AudioFileClip, VideoFileClip
    for video_path, audio_path in zip(video_path, audio_path):
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        final_clip = video.set_audio(audio)
        output: str = video_path[:-4] + "-{CONVERTED}" + video_path[len(video_path) - 4:]
        final_clip.write_videofile(output)


def rm_tmp_files(video_path: list, audio_path: list):
    """
    Remove temporary video and audio files
    """
    for video, audio in zip(video_path, audio_path):
        os.remove(video)
        os.remove(audio)


class Downloader:
    """
    Represents a class of a download manager
    """

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

    def download(self) -> None:
        """
        Check arguments and call a proper download method
        """
        if (self.args.video_only and self.args.audio_only) or (not self.args.video_only and not self.args.audio_only):
            print('Downloading file')
            self.download_file()
        elif self.args.video_only:
            self.download_video()
        elif self.args.audio_only:
            self.download_audio()

    def download_video(self) -> list[str]:
        """
        Download video only
        :return: Paths to saved video files
        :rtype: list[str]
        """
        # Absolute paths of saved video files
        paths: list = []
        for file in self.files:
            video = file.yt.streams.filter(only_video=True)
            if self.args.resolution != "":
                video = self.check_resolution(file).first()
            else:
                # Getting video in the highest resolution (in pytube case, it's 720p for whatever reason)
                video = file.yt.streams.get_highest_resolution()
            self.show_info(file, video.filesize_mb, video=True)
            # Download video and save its path to variable
            path = video.download(output_path=self.args.directory, filename=file.filename.get("video"))
            paths.append(path)
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
            self.show_info(file, audio.filesize_mb, audio=True)
            # Download audio and save its path to variable
            path = audio.download(output_path=self.args.directory, filename=file.filename.get('audio'))
            paths.append(path)
        return paths

    def download_file(self) -> None:
        """
        Download video with audio
        """
        if self.args.resolution != "" and int(self.args.resolution[:-1]) > 720:
            print('Downloading video files')
            paths_video = self.download_video()
            print('Downloading audio files')
            paths_audio = self.download_audio()
            print('Merging files together')
            concat(paths_video, paths_audio)
            print('Removing tmp files')
            rm_tmp_files(paths_video, paths_audio)
        else:
            for file in self.files:
                print('Downloading 720p video')
                down_file = file.yt.streams.get_highest_resolution()
                self.show_info(file, down_file.filesize_mb)
                down_file.download(output_path=self.args.directory, filename=file.filename.get('video'))

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
            print(f'Unfortunately, "{file.title}" with resolution {self.args.resolution} is not available')
            print('Here is a list with resolutions that are available:')
            print(get_res(file=file))
            self.args.resolution = int(input('Please, choose a resolution from the list above: '))
            self.check_resolution(file)

    def show_info(self, file: File, filesize_mb: float, video: bool = False, audio: bool = False) -> None:
        """
        Print info about download progress
        :param file: Current downloading file
        :type file: File
        :param filesize_mb: File size in MB
        :type filesize_mb: float
        :param video: Video flag
        :type video: bool
        :param audio: Audio flag
        :type audio: bool
        """
        # Video and audio argument may not be specified, but info has to be shown
        if not video and not audio:
            filename_video = file.filename.get('video')
            print(f'[INFO] Downloading file "{filename_video}",'
                  f'with size of {filesize_mb} MB, to {self.args.directory}')
        elif video:
            filename_video = file.filename.get('video')
            print(f'[INFO] Downloading video "{filename_video}",'
                  f'with size of {filesize_mb} MB, to {self.args.directory}')
        elif audio:
            filename_audio = file.filename.get('audio')
            print(f'[INFO] Downloading audio "{filename_audio}", '
                  f'with size of {filesize_mb} MB, to {self.args.directory}')
