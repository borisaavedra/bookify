import click

from books import commands as books_commands

BOOKS_TABLE = ".books.csv"

@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}
    ctx.obj["books_table"] = BOOKS_TABLE


cli.add_command(books_commands.all)