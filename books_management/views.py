from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.db.models import Q
from .models import Book, Review, Category
from .forms import BookForm, ReviewForm, CustomUserCreationForm
# Create your views here.


# Check if user is admin
def is_admin(user):
    return user.is_staff


# User Registration
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get("role")
            if role == "admin":
                user.is_staff = True
            user.save()
            login(request, user)
            return redirect("book_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


# Book List
def book_list(request):
    searchQ = request.GET.get("q")
    category_filter = request.GET.get("category")
    books = Book.objects.all()

    if searchQ:
        books = books.filter(Q(title__icontains=searchQ) | Q(author__icontains=searchQ))
    if category_filter:
        books = books.filter(category__name=category_filter)

    categories = Category.objects.all()
    return render(request, "books/book_list.html", {"books": books, "categories": categories})


# Book Detail + Add Review
def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    reviews = book.reviews.all()

    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect("book_detail", id=book.id)
    else:
        form = ReviewForm()

    context = {
        "book": book,
        "reviews": reviews, 
        "form": form
    }

    return render(request, "books/book_detail.html", context)


# Admin: Add Book
@user_passes_test(is_admin)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user  # Link book to admin 
            book.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "books/add_book.html", {"form": form})


# Admin: Update Book
@user_passes_test(is_admin)
def update_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_detail", id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, "books/update_book.html", {"form": form})


# Admin: Delete Book
@user_passes_test(is_admin)
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect("book_list")
