from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Author, Category, Book, Borrow

class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'books_count', 'created_at']
        read_only_fields = ['created_at']

    def get_books_count(self, obj) -> int:
        return obj.books.count()

class CategorySerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'books_count', 'created_at']
        read_only_fields = ['created_at']

    def get_books_count(self, obj) -> int:
        return obj.books.count()

class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'author', 'author_name', 
            'category', 'category_name', 'total_copies', 'available_copies',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, attrs):
        # Ensure available_copies doesn't exceed total_copies
        available = attrs.get('available_copies', 0)
        total = attrs.get('total_copies', 0)
        
        if available > total:
            raise serializers.ValidationError(
                "Available copies cannot exceed total copies"
            )
        return attrs

class BorrowSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    author_name = serializers.CharField(source='book.author.name', read_only=True)
    is_overdue = extend_schema_field(serializers.BooleanField)(serializers.ReadOnlyField())
    days_overdue = extend_schema_field(serializers.IntegerField)(serializers.ReadOnlyField())

    class Meta:
        model = Borrow
        fields = [
            'id', 'user', 'user_username', 'book', 'book_title', 'author_name',
            'borrow_date', 'due_date', 'return_date', 'is_overdue', 'days_overdue'
        ]
        read_only_fields = ['user', 'borrow_date', 'due_date']

class BorrowCreateSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Borrow
        fields = ['book_id']

    def validate_book_id(self, value):
        try:
            book = Book.objects.get(id=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found")
        
        if book.available_copies <= 0:
            raise serializers.ValidationError("No copies available for this book")
        
        return value

class ReturnBookSerializer(serializers.Serializer):
    borrow_id = serializers.IntegerField()

    def validate_borrow_id(self, value):
        try:
            borrow = Borrow.objects.get(id=value)
        except Borrow.DoesNotExist:
            raise serializers.ValidationError("Borrow record not found")
        
        if borrow.return_date:
            raise serializers.ValidationError("Book already returned")
        
        # Check if the user owns this borrow record
        request = self.context.get('request')
        if request and request.user != borrow.user:
            raise serializers.ValidationError("You can only return your own books")
        
        return value

class BorrowResponseSerializer(serializers.Serializer):
    """Serializer for borrow book response"""
    message = serializers.CharField()
    penalty_points_added = serializers.IntegerField()
    total_penalty_points = serializers.IntegerField()
    borrow = BorrowSerializer()

class ReturnBookResponseSerializer(serializers.Serializer):
    """Serializer for return book response"""
    message = serializers.CharField()
    penalty_points_added = serializers.IntegerField()
    total_penalty_points = serializers.IntegerField()
    borrow = BorrowSerializer()

class ErrorResponseSerializer(serializers.Serializer):
    """Serializer for error responses"""
    error = serializers.CharField()
