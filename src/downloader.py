from file import File
from arguments import Arguments
from pytube import StreamQuery
import os
import sys


# TODO: Add support for choosing FPS


def concat(video_path: list, audio_path: list) -> None:
    """
    Merge video and audio to one file
    :param video_path: Paths to video files
    :type video_path: list
    :param audio_path: Paths to audio files
    :type audio_path: list
    """
    import subprocess
    for video_path, audio_path in zip(video_path, audio_path):
        output_path = video_path[:-4] + "-{CONVERTED}" + video_path[len(video_path) - 4:]
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            output_path
        ]
        try:
            subprocess.run(cmd)
        except:
            sys.exit('FFmpeg not installed, exiting...')


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

    def generate_files(self) -> list[File]:
        """
        Create instances of File class and append them to {self.files} list

        :return: List of URLs
        """
        tmp_list: list = []
        for url in self.args.url:
            tmp_list.append(File(url, self.args.video_only, self.args.audio_only))
        return tmp_list

    def download(self) -> None:
        """
        Check arguments and start download
        """
        if (self.args.video_only and self.args.audio_only) or (not self.args.video_only and not self.args.audio_only):
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
            if self.args.resolution != "":
                video = self.check_resolution(file).first()  # Getting video in the specified resolution or the highest possible
            else:
                # Getting video in the highest resolution (in pytube case 720p)
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
            paths_video = self.download_video()
            paths_audio = self.download_audio()
            print('Merging files together')
            concat(paths_video, paths_audio)
            print('Removing temporary files')
            rm_tmp_files(paths_video, paths_audio)
            print("[DONE]")
        else:
            for file in self.files:
                down_file = file.yt.streams.get_highest_resolution()
                self.show_info(file, down_file.filesize_mb)
                down_file.download(output_path=self.args.directory, filename=file.filename.get('video'))

    def check_resolution(self, file: File) -> StreamQuery:
        """
        Check if file is available in prompted resolution.
        If not, the next highest resolution is returned.
        :param file: Currently downloading file
        :type file: File
        :return: Query with available resolution
        """
        available_resolutions = file.yt.streams.filter(res=self.args.resolution)
        if len(available_resolutions) > 0:
            print(file.title)
            print(available_resolutions)
            return available_resolutions
        else:
            print(f'Unfortunately, "{file.title}" is not available in {self.args.resolution}.')
            highest_res = file.yt.streams.filter(only_video=True, mime_type='video/mp4')
            print(f'Choosing the highest resolution: {highest_res.first().resolution}')
            print(type(highest_res))
            return highest_res

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
