import logging
import operator
from functools import reduce

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from rest_framework import generics
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .forms import BookUpdateForm, AuthorForm
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        self.user = form.get_user()
        if self.user.is_superuser:
            login(self.request, self.user)
            return super().form_valid(form)
        else:
            messages.error(self.request, 'You are not authorized to access this page.')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('author_panel')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'user') and self.user.is_superuser:
            context['admin_name'] = self.user.username
        return context

    def post(self, request, *args, **kwargs):
        if 'logout' in request.POST:
            logout(request)
            messages.success(request, 'You have been logged out successfully.')
            return redirect('login')

        return super().post(request, *args, **kwargs)


def AuthorView(request):
    authors = Author.objects.all()
    books = Book.objects.all()
    search_query = request.GET.get('q')
    if search_query:
        authors = authors.filter(
            Q(name__icontains=search_query) | Q(email__icontains=search_query) | Q(user_name__icontains=search_query)
        )

    total_authors = authors.count()
    total_books = books.count()

    paginator = Paginator(authors, 4)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
        'total_authors': total_authors,
        'total_books': total_books
    }
    return render(request, 'admin_panel.html', context)


class AddAuthor(CreateView):
    template_name = 'add_author.html'
    success_url = reverse_lazy('author_panel')
    model = Author
    form_class = AuthorForm

    def form_valid(self, form):
        if Author.objects.filter(email=form.cleaned_data['email']).exists():
            messages.error(self.request, 'Email already exists.')
            return self.form_invalid(form)
        return super().form_valid(form)


class UpdateAuthor(UpdateView):
    template_name = 'update_author.html'
    success_url = reverse_lazy('author_panel')
    model = Author
    form_class = AuthorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = get_object_or_404(Author, pk=self.kwargs['pk'])
        context['author'] = author
        return context

    def form_valid(self, form):
        instance = form.instance
        if Author.objects.exclude(pk=instance.pk).filter(email=instance.email).exists():
            messages.error(self.request, 'Email already exists.')
            return self.form_invalid(form)
        return super().form_valid(form)


class AuthorSearchView(ListView):
    model = Author
    template_name = 'search_results.html'
    context_object_name = 'authors'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            first_word = query.split()[0]

            return Author.objects.filter(
                Q(name__icontains=first_word) |
                Q(email__icontains=first_word) |
                Q(user_name__icontains=first_word)
            )
        else:
            return Author.objects.none()


def BookList(request):
    books = Book.objects.all()
    authors = Author.objects.all()

    search_query = request.GET.get('q')
    if search_query:
        books = books.filter(Q(title__icontains=search_query) | Q(author__name__icontains=search_query))

    total_books = books.count()
    total_authors = authors.count()

    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
        'total_books': total_books,
        'total_authors': total_authors
    }
    return render(request, 'book_panel.html', context)


class UpdateBook(UpdateView):
    model = Book
    form_class = BookUpdateForm
    template_name = 'update_book.html'
    success_url = reverse_lazy('list-book')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        return context


class AddBook(CreateView):
    template_name = 'add_book.html'
    model = Book
    fields = ['title', 'author']

    def form_valid(self, form):
        title = form.cleaned_data['title']
        if len(title) < 5:
            messages.error(self.request, 'Title must be at least 5 characters long.')
            return self.form_invalid(form)
        elif len(title) > 100:
            messages.error(self.request, 'Title must be at most 100 characters long.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list-book')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        return context


class BookSearchView(ListView):
    model = Book
    template_name = 'search_results_book.html'
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(title__icontains=query)
        else:
            return Book.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = "detail_author.html"
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        books = author.book_set.all()

        paginator = Paginator(books, 5)
        page_number = self.request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context['books'] = page_obj
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context['book_update_form'] = BookUpdateForm()
        return context


class DetailBookUpdateView(UpdateView):
    model = Book
    form_class = BookUpdateForm
    template_name = 'book_update.html'
    success_url = reverse_lazy('detail-author')


class AuthorsListAPIView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorSearchAPIView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)
        if query:
            search_terms = query.split()
            authors = self.queryset.filter(
                reduce(operator.and_,
                       (Q(name__icontains=term) | Q(user_name__icontains=term) | Q(email__icontains=term) for term in
                        search_terms))
            )
            serializer = self.get_serializer(authors, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)


class BookListAPIView(ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(status=True)


class BookSearchAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)
        if not query:
            return Response({"error": "Please provide a search query using the 'q' parameter."},
                            status=status.HTTP_400_BAD_REQUEST)

        books = self.queryset.filter(title__icontains=query)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)


def toggle_author_status(request, author_id):
    try:
        author = Author.objects.get(pk=author_id)
        author.status = not author.status
        author.save()
        return JsonResponse({'status': 'success', 'new_status': author.status})
    except Author.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Author not found'})
