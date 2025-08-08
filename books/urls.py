from django.urls import path
from . import views

urlpatterns = [
    # Authors
    path('authors/', views.AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    
    # Categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Books
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # Borrowing
    path('borrow/', views.borrow_book, name='borrow-book'),
    path('my-borrows/', views.list_user_borrows, name='list-user-borrows'),
    path('return/', views.return_book, name='return-book'),
]
