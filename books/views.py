from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Author, Category, Book, Borrow
from .serializers import (
    AuthorSerializer, CategorySerializer, BookSerializer, BorrowSerializer,
    BorrowCreateSerializer, ReturnBookSerializer, ReturnBookResponseSerializer,
    ErrorResponseSerializer
)
from authentication.models import User

class IsAdminOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow admins to edit objects."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

# Author Views
@extend_schema(tags=['Authors'])
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

@extend_schema(tags=['Authors'])
class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]

# Category Views
@extend_schema(tags=['Categories'])
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

@extend_schema(tags=['Categories'])
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

# Book Views
@extend_schema(tags=['Books'])
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.select_related('author', 'category').all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author', 'category']
    search_fields = ['title', 'author__name', 'category__name']
    ordering_fields = ['title', 'created_at', 'updated_at']
    ordering = ['title']

@extend_schema(tags=['Books'])
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.select_related('author', 'category').all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

# Borrowing Views
@extend_schema(
    operation_id='borrow_book',
    summary='Borrow a book',
    description='Borrow a book from the library. Users can have maximum 3 active borrows.',
    request=BorrowCreateSerializer,
    responses={
        201: BorrowSerializer,
        400: ErrorResponseSerializer,
        404: ErrorResponseSerializer
    },
    tags=['Borrowing']
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def borrow_book(request):
    serializer = BorrowCreateSerializer(data=request.data)
    if serializer.is_valid():
        book_id = serializer.validated_data['book_id']
        user = request.user
        
        # Check user's current active borrows (max 3)
        active_borrows = Borrow.objects.filter(user=user, return_date__isnull=True).count()
        if active_borrows >= 3:
            return Response({
                'error': 'You have reached the maximum borrowing limit (3 books)'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            with transaction.atomic():
                book = Book.objects.select_for_update().get(id=book_id)
                
                # Double-check availability
                if book.available_copies <= 0:
                    return Response({
                        'error': 'No copies available for this book'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Create borrow record
                borrow = Borrow.objects.create(
                    user=user,
                    book=book,
                    due_date=timezone.now() + timezone.timedelta(days=14)
                )
                
                # Update available copies
                book.available_copies -= 1
                book.save()
                
                return Response(
                    BorrowSerializer(borrow).data,
                    status=status.HTTP_201_CREATED
                )
        
        except Book.DoesNotExist:
            return Response({
                'error': 'Book not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    operation_id='list_user_borrows',
    summary='List user active borrows',
    description='Get all active borrows for the authenticated user.',
    responses={
        200: BorrowSerializer(many=True),
    },
    tags=['Borrowing']
)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_user_borrows(request):
    borrows = Borrow.objects.filter(
        user=request.user,
        return_date__isnull=True
    ).select_related('book', 'book__author')
    
    serializer = BorrowSerializer(borrows, many=True)
    return Response(serializer.data)

@extend_schema(
    operation_id='return_book',
    summary='Return a borrowed book',
    description='Return a previously borrowed book. Penalty points may be added for late returns.',
    request=ReturnBookSerializer,
    responses={
        200: ReturnBookResponseSerializer,
        400: ErrorResponseSerializer,
        404: ErrorResponseSerializer
    },
    tags=['Borrowing']
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def return_book(request):
    serializer = ReturnBookSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        borrow_id = serializer.validated_data['borrow_id']
        
        try:
            with transaction.atomic():
                borrow = Borrow.objects.select_for_update().get(id=borrow_id)
                book = Book.objects.select_for_update().get(id=borrow.book.id)
                user = User.objects.select_for_update().get(id=borrow.user.id)
                
                # Set return date
                borrow.return_date = timezone.now()
                
                # Calculate penalty if late
                penalty_points = borrow.calculate_penalty_on_return()
                if penalty_points > 0:
                    user.penalty_points += penalty_points
                    user.save()
                
                borrow.save()
                
                # Update available copies
                book.available_copies += 1
                book.save()
                
                return Response({
                    'message': 'Book returned successfully',
                    'penalty_points_added': penalty_points,
                    'total_penalty_points': user.penalty_points,
                    'borrow': BorrowSerializer(borrow).data
                })
        
        except Borrow.DoesNotExist:
            return Response({
                'error': 'Borrow record not found'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
