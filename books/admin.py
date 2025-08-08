from django.contrib import admin
from .models import Author, Category, Book, Borrow

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'total_copies', 'available_copies', 'created_at']
    list_filter = ['category', 'author', 'created_at']
    search_fields = ['title', 'author__name', 'category__name']
    ordering = ['title']
    raw_id_fields = ['author', 'category']

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'borrow_date', 'due_date', 'return_date', 'is_overdue']
    list_filter = ['borrow_date', 'due_date', 'return_date']
    search_fields = ['user__username', 'book__title']
    ordering = ['-borrow_date']
    raw_id_fields = ['user', 'book']
    readonly_fields = ['is_overdue', 'days_overdue']
    
    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'
