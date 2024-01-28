from django import forms

from .models import Book, Author


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'email', 'user_name']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title
