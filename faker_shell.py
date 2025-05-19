from library.models import Book
from faker import Faker
import random

fake = Faker()

for i in range(30):
    title = f"{fake.word().title()} Programming {i+1}"
    author = fake.name()
    isbn = f"{fake.random_number(digits=13)}"
    Book.objects.create(
        title=title,
        author=author,
        isbn=isbn
    )
