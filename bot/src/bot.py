import click

import gpt2


@click.group()
def cli():
    pass


@cli.command()
@click.option('--prefix', help='The title of the demotivational quote, e.g. Innovation')
@click.option('--input-file', help='The input file used for fine-tuning the model')
@click.option('--similarity-threshold', default=0.5)
@click.option('--nsamples', default=100)
@click.option('--length', default=30)
@click.option('--temperature', default=0.6)
@click.option('--k', default=40)
def generate(**args):
    for quote in gpt2.generate(**args):
        print(quote)
        print()


if __name__ == '__main__':
    cli()
