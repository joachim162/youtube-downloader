import sys
import os
import argparse
from pytube import YouTube


def args_parsing():
    url = ''
    download_dir = ''

    # TODO: Implement parsing arguments
    parser = argparse.ArgumentParser(description='Choosing video or audio to download')
    parser.add_argument('--url', metavar='-u', default=False, action='store', type=str, help='Specify video URL')
    parser.add_argument('--audio', default=False, action='store_true', help='Download audio only')
    args = parser.parse_args()

    if not args.url:
        url = args.url
        print(url)
    else:
        raise argparse.ArgumentTypeError('URL has not been specified')

    if os.path.isdir(sys.argv[-1]):
        pass
    if args.audio:
        download_audio(url, download_dir)
        print('download audio')
    if not args.audio:
        download_video(url, download_dir)


def download_video(url: str, download_dir: str):
    # TODO: Implement method for video download
    yt = YouTube(url)
    file = yt.streams.get_highest_resolution()
    print(type(file))
    # file.download(output_path=download_dir, filename_prefix='.mp4')


def download_audio(url: str, download_dir: str):
    # TODO: Implement method
    yt = YouTube(url)
    file = yt.streams.filter(only_audio=True)
    file = file.get_audio_only()
    file = yt.streams.get_by_itag(file.itag)
    file.download(output_path=download_dir, filename_prefix='.mp3')


def show_info(yt: YouTube.streams):
    """
    Prints out file information
    :param yt: YT video instance
    """
    # TODO: Implement method
    filesize = ''
    print(f'[INFO] Downloading file "{yt.title}", with size of {filesize}')


if __name__ == "__main__":
    args_parsing()
