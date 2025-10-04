from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Review


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ("reviewer", "Reviewer"),
        ("admin", "Admin"),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "role"]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "category", "cover_image", "description"]
       


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )
    class Meta:
        model = Review
        fields = ["rating", "comment"]
