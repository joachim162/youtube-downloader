import click


@click.command()
@click.argument('url')
def save(url):
    click.echo(url)

