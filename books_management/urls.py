from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.book_list, name="book_list"),
    path("book/<int:id>/", views.book_detail, name="book_detail"),
    path("book/edit_review/<int:id>/", views.edit_review, name="edit_review"),
    path("book/add/", views.add_book, name="add_book"),
    path("book/update/<int:id>/", views.update_book, name="update_book"),
    path("book/delete/<int:id>/", views.delete_book, name="delete_book"),
    path('login/', LoginView.as_view(template_name='user/login.html'), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),

]
