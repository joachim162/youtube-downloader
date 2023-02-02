from arguments import Arguments
from downloader import Downloader


if __name__ == '__main__':
    arg = Arguments()  # Load arguments
    downloader = Downloader(arg)  # Create downloader and pass arguments
    downloader.download()  # Start downloading
