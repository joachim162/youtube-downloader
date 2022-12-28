from file import File
from arguments import Arguments


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
        self.files: list = []

    def generate_files(self) -> None:
        """
        Create instances of File class and append them to {self.files} list
        :return: -
        :rtype: None
        """
        for url in self.args.url:
            self.files.append(File(url))

    # TODO: Create algorithm that handles batch downloads
