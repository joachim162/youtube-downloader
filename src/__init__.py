import click
from video import Video


@click.command()
@click.option('--url', '-u', required=False, help="YouTube video URL")
def get_url(url):
    click.echo(url)
    return url


@click.command()
@click.option('--file', '-f', required=False, help="Specify file path with URLs", type=click.Path(exists=True))
def get_urls(file):
    click.echo(click.format_filename(file))
    return read_file(file)


def read_file(url):
    pass


if __name__ == '__main__':
    get_url()
