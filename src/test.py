from pathlib import Path

path = r'C:\Users\holec\Desktop\test.txt'


def rename(old, new):
    print(Path(path).parent.joinpath(old))
    print(Path(path).parent.joinpath(new))


rename('test.txt', 'The Black Keys - I Got Mine.mp3')
