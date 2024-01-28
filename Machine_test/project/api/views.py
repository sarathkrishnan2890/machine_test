# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Author, Book
# from rest_framework import generics
# from rest_framework.exceptions import ValidationError
# from rest_framework import status
# from .serializers import AuthorSerializer, BookSerializer, UpdateAuthorserializer, Updatebokkserializer


# def my_view(request):
#     # Use the Author model in your view
#     authors = Author.objects.all()
#     books = Book.objects.all()
#     # ... rest of the view logic


# class AuthorAPIView(APIView):
#     def get(self, request):
#         authors = Author.objects.all()
#         books = Book.objects.all()
#         total_authors = authors.count()
#         total_books = books.count()

#         serializer = AuthorSerializer(authors, many=True)
#         data = {
#             'authors': serializer.data,
#             'total_authors': total_authors,
#             'total_books': total_books
#         }
#         return Response(data)


# class BookAPIView(APIView):
#     def get(self, request):
#         authors = Author.objects.all()
#         books = Book.objects.all()
#         total_authors = authors.count()
#         total_books = books.count()
#         serializer = BookSerializer(books, many=True)
#         data = {
#             'authors': serializer.data,
#             'total_authors': total_authors,
#             'total_books': total_books
#         }
#         return Response(data)


# class UpdateBook(generics.RetrieveUpdateAPIView):
#     serializer_class = Updatebokkserializer
#     queryset = Book.objects.all()


# class UpdateAuthor(generics.RetrieveUpdateAPIView):
#     serializer_class = UpdateAuthorserializer
#     queryset = Author.objects.all()


# class BookSearchAPIView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

#     def get(self, request, *args, **kwargs):
#         query = request.query_params.get('q', None)
#         if query:
#             books = self.queryset.filter(title__icontains=query)
#             serializer = self.get_serializer(books, many=True)
#             return Response(serializer.data)
#         else:
#             return Response({"error": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)


# class AuthorSearchAPIView(generics.ListAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer

#     def get(self, request, *args, **kwargs):
#         query = request.query_params.get('q', None)
#         if query:
#             authors = self.queryset.filter(name__icontains=query) | \
#                       self.queryset.filter(user_name__icontains=query) | \
#                       self.queryset.filter(email__icontains=query)
#             serializer = self.get_serializer(authors, many=True)
#             return Response(serializer.data)
#         else:
#             return Response({"error": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)


# class AuthorDetailView(generics.RetrieveAPIView):
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)

#         books = Book.objects.filter(author=instance)
#         book_serializer = BookSerializer(books, many=True)

#         data = serializer.data
#         data['books'] = book_serializer.data

#         return Response(data)


# class CreateBook(generics.CreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = Updatebokkserializer

#     def perform_create(self, serializer):
#         author_id = self.request.data.get("author")
#         try:
#             author = Author.objects.get(pk=author_id)
#             serializer.save(author=author)
#         except Author.DoesNotExist:
#             raise ValidationError("Author does not exist.")


# class CreateAuthor(generics.CreateAPIView):
#     queryset = Author.objects.all()
#     serializer_class = UpdateAuthorserializer

#     def perform_create(self, serializer):
#         email = serializer.validated_data.get('email')
#         if Author.objects.filter(email=email).exists():
#             raise ValidationError("Author with this email already exists.")
#         serializer.save()
