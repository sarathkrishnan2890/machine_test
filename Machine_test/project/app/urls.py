from django.urls import path

from .views import AuthorDetailView, AuthorSearchAPIView, AuthorsListAPIView, BookListAPIView, \
    BookSearchAPIView, CustomLoginView, AuthorView, AddAuthor, DetailBookUpdateView, \
    UpdateAuthor, BookList, UpdateBook, AddBook, BookSearchView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLoginView.as_view(), name='logout'),
    path('author-panel/', AuthorView, name='author_panel'),
    path('add-author/', AddAuthor.as_view(), name='add-author'),
    path('update-author/<int:pk>/', UpdateAuthor.as_view(), name='update-author'),
    path('author-panel/search/', AuthorView, name='author-search'),
    path('update-book/<int:pk>/', UpdateBook.as_view(), name='updbk'),
    path('add-book/', AddBook.as_view(), name='add-book'),
    path('book_list/', BookList, name='list-book'),
    path('search-book/', BookSearchView.as_view(), name='book-results'),
    path('author-detail/<int:pk>/', AuthorDetailView.as_view(), name='detail-author'),
    path('book/<int:pk>/update/', DetailBookUpdateView.as_view(), name='book_update'),
    path('authors/', AuthorsListAPIView.as_view(), name='authors-list-api'),
    path('authors/search/', AuthorSearchAPIView.as_view(), name='search-authors-api'),
    path('books/', BookListAPIView.as_view(), name='books-list-api'),
    path('books/search/', BookSearchAPIView.as_view(), name='search-books-api'),
    # path('toggle_author_status/<int:author_id>/', toggle_author_status, name='toggle_author_status'),

]
