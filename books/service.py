import csv
import os

from books.models import Books

class BooksServices:

    def __init__(seft, book_table):
        seft.book_table = book_table

    
    def create_book (seft, book):
        with open(seft.book_table, mode="a") as file:
            write = csv.DictWriter(file, fieldnames=Books.schema())
            write.writerow(book.to_dict())
    
    
    def list_books(seft):
        with open(seft.book_table, mode="r") as file:
            reader = csv.DictReader(file, fieldnames=Books.schema())

            return list(reader)


    def edit_book(seft, book_updated):
        books = seft.list_books()

        updated_books = []
        for book in books:
            if book["uid"] == book_updated.uid:
                updated_books.append(book_updated.to_dict())
            else:
                updated_books.append(book)

        seft._save_to_disk(updated_books)


    def search_book_by(seft, book_list, search_list):

        founded = []

        for book in book_list:
            for item in search_list:
                for x in item:
                    if item[x] in book[x]:
                        founded.append(book)
       
        temp = []

        for book in founded:
           if book not in temp:
               temp.append(book)

        return temp


    def delete_book(seft, book):
        books = seft.list_books()

        for item in books:
            if item["uid"] == book.uid:
                books.remove(book.to_dict())

        seft._save_to_disk(books)



    def _save_to_disk(seft,books):
        tmp_table_name = seft.book_table + ".tmp"
        
        with open(tmp_table_name, mode="w") as file:
            writer = csv.DictWriter(file, fieldnames= Books.schema())
            writer.writerows(books)

        os.remove(seft.book_table)
        os.rename(tmp_table_name,seft.book_table)