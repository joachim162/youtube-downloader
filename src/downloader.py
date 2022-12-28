from file import File
from arguments import Arguments
from pytube import YouTube, Stream, StreamQuery
from converter import concat


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


def format_title(file: File, video: bool = False, audio: bool = False) -> str:
    """
    Formatting title

    :param file:
    :type file: File
    :param video: flag for video
    :param audio: flag for audio
    :return: None
    """
    # TODO: Recode the method to return the new title
    title = file.title
    if video:
        new_title = format_title_helper(title)
        if '.mp4' not in new_title:
            new_title += '.mp4'
            print(f'video title: {new_title}')
            return new_title
    elif audio:
        new_title = format_title_helper(title)
        if '.mp4' in new_title:
            new_title = new_title[:-3]  # Removing .mp4 from audio file
            new_title += '.mp3'
        elif '.mp3' not in title:
            title += '.mp3'
        return new_title


class Downloader:
    """
    Represents a class of download manager
    """

    def __init__(self, args: Arguments):
        """

        :param args: arguments from CLI
        :type args: Arguments
        """
        self.args: Arguments = args
        self.files: list = self.generate_files()

    def generate_files(self) -> list:
        """
        Create instances of File class and append them to {self.files} list
        :return: -
        :rtype: None
        """
        tmp_list: list = []
        for url in self.args.url:
            tmp_list.append(File(url))
        return tmp_list

    # TODO: Create an algorithm that handles batch downloads
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
            self.show_info()
            format_title(file=file, video=True)
            video.download(output_path=self.args.directory, filename=format_title(video=True))

    def download_audio(self):
        pass

    def download_file(self):
        pass

    def check_resolution(self, file: File) -> StreamQuery:
        available_resolutions = file.yt.streams.filter(res=self.args.resolution)
        if len(available_resolutions) > 0:
            return available_resolutions
        else:
            print(f'Unfortunately, {file.title} with resolution {self.args.resolution} is not available')
            print('Here is a list with resolutions that are available:')
            print(self.get_res())
            self.args.resolution = input('Please, choose a resolution from the list above: ')
            self.check_resolution(file)

    def get_res(self) -> list:
        pass

    def show_info(self) -> None:
        pass

