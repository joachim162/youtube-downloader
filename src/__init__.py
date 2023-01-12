from arguments import Arguments
from downloader import Downloader
from file import File

if __name__ == '__main__':
    arg = Arguments()
    downloader = Downloader(arg)
    downloader.download()
