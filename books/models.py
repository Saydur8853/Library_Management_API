from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

class Author(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

class Book(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.author.name}"
    
    class Meta:
        ordering = ['title']
    
    def save(self, *args, **kwargs):
        # Ensure available_copies doesn't exceed total_copies
        if self.available_copies > self.total_copies:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)

class Borrow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrows')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrows')
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"
    
    class Meta:
        ordering = ['-borrow_date']
    
    def save(self, *args, **kwargs):
        # Set due date to 14 days from borrow date if not set
        if not self.due_date:
            self.due_date = self.borrow_date + timedelta(days=14)
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        if self.return_date:
            return False
        return timezone.now() > self.due_date
    
    @property
    def days_overdue(self):
        if not self.is_overdue:
            return 0
        return (timezone.now() - self.due_date).days
    
    def calculate_penalty_on_return(self):
        """Calculate penalty points if book is returned late"""
        if not self.return_date:
            return 0
        
        if self.return_date > self.due_date:
            days_late = (self.return_date - self.due_date).days
            return days_late  # 1 point per day late
        return 0
