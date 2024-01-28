from django.db import models


class Author(models.Model):
    user_name = models.CharField(max_length=100, default='null')
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.IntegerField(blank=True, default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    Book_id = models.CharField(max_length=100, default='0000')
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title
