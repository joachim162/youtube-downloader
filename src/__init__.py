from arguments import Arguments
from file import File
from downloader import Downloader

if __name__ == '__main__':
    arg = Arguments()
    downloader = Downloader(arg.check_arguments())
    downloader.download()
