from library.models import Book, BorrowHistory
from django.shortcuts import get_object_or_404

def get_all_books():
    return  Book.objects.all()

# def get_book_by_id(book_id: int) -> Book:
#     return get_object_or_404(Book, id=book_id)

# def get_borrow_history_for_book(book: Book):
#     return book.borrow_history.order_by('-borrowed_at')


from library.models import Book
from library.exceptions import BookNotFound, BookHasNoBorrowHistory

def get_book_by_id(book_id: int) -> Book:
    try:
        return Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        raise BookNotFound(f"ID {book_id}에 해당하는 책이 없습니다.")

def get_borrow_history_for_book(book: Book):
    histories = book.borrow_history.order_by('-borrowed_at')
    if not histories:
        raise BookHasNoBorrowHistory(f"'{book.title}' 도서에는 대출 이력이 없습니다.")
    return histories
