from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.text import slugify
from django.utils import timezone
# Create your models here.

def books_img_directory_name(instance, filename):
    folder_name = slugify(instance.title)  # removes spaces, special characters
    return os.path.join('books_management/media', folder_name, filename)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books")
    cover_image = models.ImageField(upload_to=books_img_directory_name, blank=True, null=True)
    description = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="added_books")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum(review.rating for review in reviews) / reviews.count(), 1)
        else:
            return None


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=1)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        
    def was_updated(self):
        """Return True if the review was updated after creation."""
        if self.updated_at:
            return self.updated_at > self.created_at
        return False

    def __str__(self):
        return f"{self.user.username}: review on '{self.book.title}'"
