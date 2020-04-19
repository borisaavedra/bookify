import click
from beautifultable import BeautifulTable

from books.service import BooksServices
from books.models import Books

@click.group()
def books():
    """Handle my books"""
    pass


@books.command()
@click.option("-n", "--name",
                type=str,
                prompt=True,
                help="The book name")
@click.option("-a", "--author",
                type=str,
                prompt=True,
                help="The author's name")
@click.option("-y", "--year",
                type=str,
                prompt=True,
                help="The year when the book was publish")
@click.option("-p", "--publisher",
                type=str,
                prompt=True,
                help="The name of the publish agency")
@click.option("-t", "--topic",
                type=str,
                prompt=True,
                help="Topic's book")
@click.pass_context
def create(ctx, name, author, year, publisher, topic):
    """Creates a Book"""
    book = Books(name, author, year, publisher, topic)
    book_service = BooksServices(ctx.obj["books_table"])

    try:
        book_service.create_book(book)
        click.echo("The book was added")
    except:
        click.echo("Something failed. Please try again")


@books.command()
@click.pass_context
def list(ctx):
    """List all Books"""
    book_service = BooksServices(ctx.obj["books_table"])
    book_list = book_service.list_books()

    _print_list(book_list)


@books.command()
@click.argument("book_uid",
                type=str)
@click.pass_context
def edit(ctx, book_uid):
    """Edits a Book"""
    book_service = BooksServices(ctx.obj["books_table"])

    books_list = book_service.list_books()

    book = [book for book in books_list if book["uid"] == book_uid]

    if book:
        book = _update_book_flow(Books(**book[0]))
        book_service.edit_book(book)
        click.echo("Book updated")
    else:
        click.echo("Book not found")

def _update_book_flow(book):
    click.echo("Leave empty if you don't want to modify the value")

    book.name = click.prompt("New name",type=str,default=book.name)
    book.author = click.prompt("New author",type=str,default=book.author)
    book.year = click.prompt("New year",type=str,default=book.year)
    book.publisher = click.prompt("New publisher",type=str,default=book.publisher)
    book.topic = click.prompt("New topic",type=str,default=book.topic)

    return book


@books.command()
@click.argument("book_id",
                type=str)
@click.pass_context
def delete(ctx, book_id):
    """Delete a Book"""
    book_service = BooksServices(ctx.obj["books_table"])

    books_list = book_service.list_books()

    book = [book for book in books_list if book["uid"] == book_id]

    if book:
        book = Books(**book[0])
        book_service.delete_book(book)
        click.echo("Book deleted")
    else:
        click.echo("Book not found")


@books.command()
@click.option("-a", "--author",
                type=str,
                # prompt=True,
                help="Author of the book") 
@click.option("-n", "--name",
                type=str,
                # prompt=True,
                help="The name of the book")        
@click.pass_context
def search(ctx, author, name):
    """Search a Book"""
    book_service = BooksServices(ctx.obj["books_table"])

    books_list = book_service.list_books()

    if author:
        founded = book_service.search_book_by(books_list, author)
    # if name:
    #     founded = book_service.search_book_by(books_list, name)
    
    if founded:
        _print_list(founded)
    else:
        click.echo("Book not found")


def _print_list(book_list):

    table = BeautifulTable()
    headers = [name.upper() for name in Books.schema()]
    table.column_headers = headers

    for book_item in book_list:
        table.append_row([book_item["name"],
                        book_item["author"],
                        book_item["year"],
                        book_item["publisher"],
                        book_item["topic"],
                        book_item["uid"]])

    # This was an effort for padding the columns
    # max_len = 0
    # for i in table["NAME"]:
    #     if len(str(i)) >= max_len:
    #         max_len = len(str(i))

    # table.set_padding_widths(5)
    # # table.left_padding_widths["NAME"] = mayor - len("NAME")
    # # table.right_padding_widths["NAME"] = mayor - len("NAME")

    click.echo(table)

all = books