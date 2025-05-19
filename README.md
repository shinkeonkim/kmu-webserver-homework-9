[웹서버컴퓨팅 과제 9] Django 기반 도서 대출 시스템의 서비스 레이어 분리 및 예외 처리
## 🔍 과제 주안점:

- View-Logic 분리 구조
- ORM 함수의 책임 분리 (조회 vs 표현)
- 단위 테스트로 검증 가능한 서비스 구조
- 사용자 정의 예외 처리 설계

과제 구성 설명 
1. 클래스 메소드 vs 서비스 레이어 비교 
2. 클래스 메소드 [이전 과제 5] vs 서비스 레이어의 구분 (이전 과제 5와 비교) 
3.  뷰(View)와 서비스(Service Layer) 분리에 사용된 ORM
4.  가장 자주 쓰는 Django ORM 명령어 
7.  책(Book) 데이터 자동 생성
8.  대출 이력(BorrowHistory) 자동 생성  
9.  예외 처리 포함 서비스 함수 
10.  Django에서의 예외 클래스(Exception Class)
11.  사용자 정의 예외
12.  단위 테스트
13. 과제 결과 화면  

✅ 깃허브 제출 링크 : 1점

과제 코딩 채워넣기 부분 : 총 39점

5.  뷰(View) 와 서비스(Service Layer) 분리 이점 : 총 6점 
✅ 2. 서비스 코드 (services/book_service.py) : 3점 

```python
def get_all_books():
    return  Book.objects.all()

def get_book_by_id(book_id: int) -> Book:
    return get_object_or_404(Book, id=book_id)

def get_borrow_history_for_book(book: Book):
    return book.borrow_history.order_by('-borrowed_at')
```

✅ 3. 뷰 코드 (views.py) — 서비스 호출만 수행 : 3점

```python
from django.shortcuts import render
from library.services import book_service

def book_list(request):
 books = book_service.get_all_books()
 return render(request, 'library/book_list.html', {'books': books})

def book_history(request, book_id):
    book = book_service.get_book_by_id(book_id)
    histories = book_service.get_borrow_history_for_book(book)
    
    return render(request, 'library/book_history.html', {
       'book': book,
       'histories': histories,
    })
```

6.  뷰(View) 와 서비스(Service Layer) 분리 예제 : 총 8점 
✅ URL 설정 — library/urls.py : 3점 
```python
# library/urls.py
from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/history/', views.book_history, name='book_history'),
]
```

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/', include('library.urls')),
]
```

✅ 뷰 구현 — views.py  : 3점

```python
from django.shortcuts import render, get_object_or_404
from .models import Book


def book_list(request):
 books = Book.objects.all()
 return render(request, 'library/book_list.html', {'books': books})

def book_history(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    histories = book.borrow_history.order_by('-borrowed_at')
    
    return render(request, 'library/book_history.html', {
       'book': book,
       'histories': histories,
    })
```



✅ 템플릿 생성 :  2점 

library/templates/library/book_list.html

```html
<h1>📚 책 목록</h1>
<ul>
    {% for book in books %}
        <li>
            <a href= "{% url 'library:book_history' book.id %}">
            {{ book.title }} by {{ book.author }}
            </a>
        </li>
    {% empty %}
        <li>등록된 책이 없습니다.</li>
    {% endfor %}
</ul>
```

library/templates/library/book_history.html

```html
<h2>📖 대출 이력: {{ book.title }}</h2>
<ul>
    {% for history in histories %}
        <li>
            {{ history.user.username }} - {{ history.borrowed_at|date:"Y-m-d H:i" }}
            {% if history.returned_at %}
                (반납: {{ history.returned_at|date:"Y-m-d" }})
            {% else %}
                🕒 미반납
            {% endif %}
        </li>
    {% empty %}
        <li>대출 이력이 없습니다.</li>
    {% endfor %}
</ul>
<a href="{% url 'library:book_list' %}">← 책 목록으로</a>
```

9.  예외 처리 포함 서비스 함수 : 총 6점  
✅ 서비스 레이어 예제 (services/book_service.py) : 4점 
```python
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
```


✅ 뷰 예제 (views.py)에서의 예외 처리 : 2점  


```python
from django.shortcuts import render
from django.http import HttpResponseNotFound
from library.services import book_service
from library.exceptions import BookNotFound, BookHasNoBorrowHistory

def book_history(request, book_id):
   try:
      book = book_service.get_book_by_id(book_id)
      histories = book_service.get_borrow_history_for_book(book)
   except BookNotFound as e:
      return HttpResponseNotFound(str(e))
   except BookHasNoBorrowHistory as e:
      return render(request, 'library/no_history.html', {'message': str(e)})
   
   return render(request, 'library/book_history.html', {
      'book': book,
      'histories': histories,
   })
```

12.  단위 테스트 : 총 15점 
✅ 테스트 코드 예시: tests/test_services.py : 6점

```python
# library/tests/test_services.py
import pytest
from library.models import Book
from library.services import get_book_by_id
from library.exceptions import BookNotFound

@pytest.mark.django_db
def test_get_book_by_id_success():
    # Given
    book = Book.objects.create(title='Test Book', author='Tester', isbn='1234567890123')
    
    # When
    result = get_book_by_id(book.id)
    # Then
    assert result == book
    assert result.title == 'Test Book'

@pytest.mark.django_db
def test_get_book_by_id_not_found():
    # When & Then
    with pytest.raises(BookNotFound) as exc_info:
        get_book_by_id(9999)
    assert "ID 9999에 해당하는 책이 없습니다." in str(exc_info.value)
```

✅ 3. 테스트 코드 (tests/test_services.py) : 9점  
```python
import pytest
from django.contrib.auth.models import User
from library.models import Book, BorrowHistory
from library.services.book_service import get_borrow_history_for_book
from library.exceptions import BookHasNoBorrowHistory

@pytest.mark.django_db
def test_get_borrow_history_for_book_success():
    # Given
    user = User.objects.create(username='testuser')
    book = Book.objects.create(title='Test Book', author='Tester', isbn='1234567890123')
    BorrowHistory.objects.create(book=book, user=user)

    # When
    histories = get_borrow_history_for_book(book)
    
    # Then
    assert histories.count() == 1
    assert histories.first().user == user

@pytest.mark.django_db
def test_get_borrow_history_for_book_no_history():
    # Given
    book = Book.objects.create(title='Empty Book', author='Nobody', isbn='9999999999999')
    
    # When & Then
    with pytest.raises(BookHasNoBorrowHistory) as exc_info:
        get_borrow_history_for_book(book)
    assert '도서에는 대출 이력이 없습니다.' in str(exc_info.value)
```

13.  결과 확인 : 총 4점  
✅ 전체 책 목록 보기 화면 캡쳐 : 1점   
✅ 특정 책의 대출 이력 확인 (대출 이력이 없는 경우 화면 캡쳐)  : 1점  
✅ 특정 책의 대출 이력 확인 (대출 이력이 있는 경우 화면 캡쳐)  : 1점 
✅ 단위 테스트 결과 성공 화면 캡쳐 : 1점   
