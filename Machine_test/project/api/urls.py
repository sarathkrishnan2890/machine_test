# from django.urls import path

# from .views import AuthorAPIView, AuthorDetailView, BookAPIView, BookSearchAPIView, CreateAuthor, CreateBook, \
#     UpdateBook, UpdateAuthor, AuthorSearchAPIView

# urlpatterns = [
#     path('authors/', AuthorAPIView.as_view(), name='author-api'),
#     path('books/', BookAPIView.as_view(), name='book-api'),
#     path('update-book/<int:pk>/', UpdateBook.as_view(), name='update-book'),
#     path('update-author/<int:pk>/', UpdateAuthor.as_view(), name='update_author'),
#     path('books/search/', BookSearchAPIView.as_view(), name='book-search-api'),  # books/search/?q={your query}
#     path('author/search/', AuthorSearchAPIView.as_view(), name='author-search-api'),
#     path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
#     path('books/create/', CreateBook.as_view(), name='create-book'),
#     path('authors/create/', CreateAuthor.as_view(), name='create-author'),

# ]
