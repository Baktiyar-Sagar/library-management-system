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
        exclude = [ 'added_by' , 'created_at' , 'updated_at'   ]
        widgets = {
                'title': forms.TextInput(attrs={
                    'class': 'input input-bordered w-full',
                    'placeholder': 'Enter book title'
                }),
                'author': forms.TextInput(attrs={
                    'class': 'input input-bordered w-full',
                    'placeholder': 'Enter author name'
                }),
                'category': forms.Select(attrs={
                    'class': 'select select-bordered w-full'
                }),
                'description': forms.Textarea(attrs={
                    'class': 'textarea textarea-bordered w-full',
                    'placeholder': 'Enter book description'
                }),
                'cover_image': forms.ClearableFileInput(attrs={
                    'class': 'file-input file-input-success file-input-primary w-full'
                }),
            }


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect
    )
    class Meta:
        model = Review
        fields = ["rating", "comment"]
