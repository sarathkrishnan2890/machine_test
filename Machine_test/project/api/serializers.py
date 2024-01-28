# from rest_framework import serializers
# from .models import Author, Book


# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields = ['title', 'author', 'published_date', 'status']


# class AuthorSerializer(serializers.ModelSerializer):
#     books = BookSerializer(many=True, read_only=True)

#     class Meta:
#         model = Author
#         fields = ['id', 'name', 'email', 'user_name', 'books']


# class Updatebokkserializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ['title', 'author']
#         model = Book


# class UpdateAuthorserializer(serializers.ModelSerializer):
#     class Meta:
#         fields = ['name', 'email', 'user_name']
#         model = Author
