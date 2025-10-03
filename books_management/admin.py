from django.contrib import admin

# Register your models here.
from .models import Book, Review, Category

# admin.site.register(Book)
# admin.site.register(Review)
# admin.site.register(Category)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "added_by", "created_at")
    list_filter = ("category", "added_by")
    search_fields = ("title", "author")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "rating", "created_at")
    search_fields = ("book__title", "user__username", "comment")
