from django.shortcuts import render, redirect
from books.models import Book


def index(request):
    return redirect('books', permanent=False)

def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all().order_by('-pub_date')
    context = {
        'books': books
    }
    return render(request, template, context)


def books_by_date_view(request, pub_date):
    template = 'books/books_list.html'

    current_date = pub_date.date() if hasattr(pub_date, 'date') else pub_date

    books = Book.objects.filter(pub_date=current_date)

    dates = Book.objects.values_list('pub_date', flat=True).distinct().order_by('pub_date')

    prev_date = None
    for date in dates:
        if date < current_date:
            prev_date = date
        else:
            break

    next_date = None
    for date in reversed(dates):
        if date > current_date:
            next_date = date
        else:
            break

    context = {
        'books': books,
        'prev_date': prev_date,
        'next_date': next_date,
    }
    return render(request, template, context)