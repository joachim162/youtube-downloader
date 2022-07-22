import sys
import os
import argparse
from pytube import YouTube, Stream


def args_parsing() -> None:
    parser = argparse.ArgumentParser(description='Choosing video or audio to download')
    parser.add_argument('--url', '-u', required=True, default=False, action='store', type=str,
                        help='Specify video URL')
    parser.add_argument('--audio', default=False, required=False, action='store_true', help='Download audio only')
    parser.add_argument('--resolution', '-r', required=False, action='store', type=str, help='Specify video '
                                                                                             'resolution (1080p)')
    parser.add_argument('dir', nargs='?', default=os.getcwd(), help='Directory for downloaded file')
    args = parser.parse_args()
    check_parsing(args)


def check_parsing(args) -> None:
    """
    Check parsing and start downloading
    :param args: Command line arguments
    :return: None
    """
    download_dir = ''
    resolution = ''
    if os.path.isdir(sys.argv[-1]):
        download_dir = sys.argv[-1]
    if args.audio:
        download_audio(args.url, download_dir)
    if not args.audio:
        if len(args.resolution) > 0:
            resolution = args.resolution
        download_video(args.url, download_dir, resolution)


def check_resolution(res: str, yt: YouTube) -> Stream:
    """
    Check resolution format
    :param yt: YouTube video
    :param res: Video resolution
    :return: New file stream containing video with specified resolution, if resolution is specified
    """
    res.lower()
    file = yt.streams.filter(res=res, progressive=True)

    # Checking if :param res is valid and video with that resolution exists
    if len(res) > 0 and len(yt.streams.filter(res=res)) > 0:
        return file
    else:
        print(f'[INFO] Video is not available in {res} resolution')
        user_input = input('Do you want to download video in maximum resolution? (Y/n)\n')
        user_input.lower()

        # Checking whether the :param user_input is valid or not
        while not user_input.__eq__('y') or not user_input.__eq__('n'):
            print('Unknown operation, please try again')
            user_input = input('Do you want to download video in maximum resolution? (Y/n)\n')
            user_input.lower()

            # If true, video with maximum resolution will be downloaded
            if user_input.__eq__('y'):
                # TODO: Get video resolution
                vid_res = ''
                print(f'Video will be downloaded in {vid_res} resolution')
                return yt.streams.get_highest_resolution()
            else:
                new_res: str = input('Please input new resolution: ')
                check_resolution(new_res, yt)


def download_video(url: str, download_dir: str, resolution: str) -> None:
    """"
    Downloads video and audio
    :param resolution: Video resolution
    :param url: Video URL
    :param download_dir: Target directory
    :return: None
    """
    yt = YouTube(url)
    file = check_resolution(resolution, yt)
    file = yt.streams.get_by_itag(file[0].itag)  # Getting tag of first video
    show_info(file, f'{file.title}.mp4')  # Printing additional information about video
    file.download(output_path=download_dir)  # Downloading video


def download_audio(url: str, download_dir: str):
    """
    Downloads audio only
    :param url: Video URL
    :param download_dir: Target directory
    :return: None
    """
    yt = YouTube(url)
    file = yt.streams.filter(only_audio=True)
    file = file.get_audio_only()
    file = yt.streams.get_by_itag(file.itag)
    filename = file.title[:-4]  # Removing last 4 chars, audio file has from unknown reason .mp4 suffix
    filename += '.mp3'
    show_info(file, filename)
    file.download(output_path=download_dir, filename=filename)


def show_info(yt, filename: str):
    """
    Prints out file information
    :param filename: Modified file name with proper file suffix
    :param yt: YT video instance
    """
    # TODO: Implement progress bar
    file_size: int = round(yt.filesize / 1024 ** 2, 2)  # File size in MB
    print(f'[INFO] Downloading "{yt.title}", with size of {file_size} MB, in {filename[-3:]} format')


if __name__ == "__main__":
    args_parsing()
