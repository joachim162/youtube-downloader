from file import File
from arguments import Arguments
from pytube import YouTube, Stream, StreamQuery
from converter import concat


def help_format_name(filename: str) -> str:
    """
    Remove unwanted characters from file name
    :param filename: File name to format
    :type filename: str
    :return: Formatted file name
    :rtype: str
    """
    filename = filename.strip()
    filename = filename.replace('"', '')
    filename = filename.replace(' ', '_')
    filename = filename.replace('/', '')
    filename = filename.replace("'", "")
    return filename


def format_name(file: File, index: int, video: bool = False, audio: bool = False) -> str:
    # TODO: Implement a function, that if an index is greater than zero, index will be added to the file name
    """
    Reformat file name
    :param index: Current index of file in a for loop of download methods
    :type index: int
    :param file: Current downloading file
    :type file: File
    :param video: Flag that indicates video
    :type video: bool
    :param audio: Flag that indicates audio
    :type audio: bool
    :return:
    :rtype:
    """
    title = file.title
    if video:
        new_title = help_format_name(title)
        if '.mp4' not in new_title:
            new_title += '.mp4'
            print(f'video title: {new_title}')
            return new_title
    elif audio:
        new_title = help_format_name(title)
        if '.mp4' in new_title:
            new_title = new_title[:-3]  # Removing .mp4 from audio file
            new_title += '.mp3'
        elif '.mp3' not in title:
            title += '.mp3'
            print(f'audio title: {new_title}')
        return new_title


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


class Downloader:
    """
    Represents a class of a download manager
    """
    index = 0  # Index of current downloading file

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
            tmp_list.append(File(url))
        return tmp_list

    # TODO: Create an algorithm that handles batch downloads
    # TODO: Add a reaction to situation where arguments for video and audio only are both True
    def download(self):
        if self.args.video_only:
            self.download_video()
        elif self.args.audio_only:
            self.download_audio()
        else:
            self.download_file()

    def download_video(self):
        for file in self.files:
            video = file.yt.streams.filter(only_video=True)
            if self.args.resolution is not "":
                video = self.check_resolution(file.yt).first()
            else:
                # Getting video in the highest resolution (in pytube case, it's 720p for whatever reason)
                video = file.yt.streams.get_high_resolution()
            self.show_info(file, video.filesize, video=True)
            # TODO: In case of downloading multiple files, filename should contain a number increasing
            #  by 1 with every iteration
            video.download(output_path=self.args.directory, filename=format_name(file, self.index, video=True))
            self.index += 1

    def download_audio(self):
        for file in self.files:
            audio = file.yt.streams.filter(only_audio=True)
            audio = audio.get_audio_only()
            audio = file.yt.streams.get_by_itag(audio.itag)
            self.show_info(file, audio.filesize, audio=True)
            # TODO: In case of downloading multiple files, filename should contain a number increasing
            #  by 1 by every iteration
            audio.download(output_path=self.args.directory, filename=self.args.output)
            self.index += 1

    def download_file(self):
        for file in self.files:
            pass

    def check_resolution(self, file: File) -> StreamQuery:
        available_resolutions = file.yt.streams.filter(res=self.args.resolution)
        if len(available_resolutions) > 0:
            return available_resolutions
        else:
            print(f'Unfortunately, {file.title} with resolution {self.args.resolution} is not available')
            print('Here is a list with resolutions that are available:')
            print(get_res(file=file))
            self.args.resolution = input('Please, choose a resolution from the list above: ')
            self.check_resolution(file)

    def show_info(self, file: File, file_size: float, video: bool = False, audio: bool = False) -> None:
        """
        Print info about download progress

        :param file: Current downloading file
        :type file: File
        :param file_size: File size
        :type file_size: float
        :param video: Video flag
        :type video: bool
        :param audio: Audio flag
        :type audio: bool
        :return: None
        :rtype: None
        """
        file_size: int = round(file_size / 1024 ** 2, 2)  # Converting file size to MB and rounding to 2 decimal places
        if video:
            print(f'[INFO] Downloading video "{file.title}", '
                  f'with size of {file_size} in MB, to {self.args.directory}')
        elif audio:
            print(f'[INFO] Downloading audio "{file.title}", '
                  f'with size of {file_size} in MB, to {self.args.directory}')

