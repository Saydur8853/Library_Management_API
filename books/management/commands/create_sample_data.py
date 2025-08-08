from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from books.models import Author, Category, Book

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample data for the library management system'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin/admin123'))
        
        # Create sample user
        if not User.objects.filter(username='user').exists():
            User.objects.create_user('user', 'user@example.com', 'user123')
            self.stdout.write(self.style.SUCCESS('Created user: user/user123'))
        
        # Create authors
        authors_data = [
            {'name': 'J.K. Rowling', 'bio': 'British author, best known for the Harry Potter series.'},
            {'name': 'George Orwell', 'bio': 'English novelist and essayist, journalist and critic.'},
            {'name': 'Agatha Christie', 'bio': 'English writer known for her detective novels.'},
            {'name': 'Stephen King', 'bio': 'American author of horror, supernatural fiction, suspense, and fantasy novels.'},
            {'name': 'Jane Austen', 'bio': 'English novelist known primarily for her six major novels.'}
        ]
        
        authors = []
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(**author_data)
            if created:
                authors.append(author)
                self.stdout.write(f'Created author: {author.name}')
        
        # Create categories
        categories_data = [
            {'name': 'Fiction'},
            {'name': 'Mystery'},
            {'name': 'Fantasy'},
            {'name': 'Horror'},
            {'name': 'Classic Literature'},
            {'name': 'Science Fiction'},
            {'name': 'Romance'}
        ]
        
        categories = []
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            if created:
                categories.append(category)
                self.stdout.write(f'Created category: {category.name}')
        
        # Create books
        if authors and categories:
            fiction = Category.objects.get(name='Fiction')
            fantasy = Category.objects.get(name='Fantasy')
            mystery = Category.objects.get(name='Mystery')
            horror = Category.objects.get(name='Horror')
            classic = Category.objects.get(name='Classic Literature')
            
            rowling = Author.objects.get(name='J.K. Rowling')
            orwell = Author.objects.get(name='George Orwell')
            christie = Author.objects.get(name='Agatha Christie')
            king = Author.objects.get(name='Stephen King')
            austen = Author.objects.get(name='Jane Austen')
            
            books_data = [
                {
                    'title': "Harry Potter and the Philosopher's Stone",
                    'description': "The first novel in the Harry Potter series.",
                    'author': rowling,
                    'category': fantasy,
                    'total_copies': 5,
                    'available_copies': 5
                },
                {
                    'title': '1984',
                    'description': "A dystopian social science fiction novel.",
                    'author': orwell,
                    'category': fiction,
                    'total_copies': 3,
                    'available_copies': 3
                },
                {
                    'title': 'Murder on the Orient Express',
                    'description': "A detective novel featuring Hercule Poirot.",
                    'author': christie,
                    'category': mystery,
                    'total_copies': 4,
                    'available_copies': 4
                },
                {
                    'title': 'The Shining',
                    'description': "A horror novel about a writer who becomes the caretaker of an isolated hotel.",
                    'author': king,
                    'category': horror,
                    'total_copies': 2,
                    'available_copies': 2
                },
                {
                    'title': 'Pride and Prejudice',
                    'description': "A romantic novel of manners.",
                    'author': austen,
                    'category': classic,
                    'total_copies': 3,
                    'available_copies': 3
                },
                {
                    'title': 'Animal Farm',
                    'description': "An allegorical novella about farm animals who rebel against their human farmer.",
                    'author': orwell,
                    'category': fiction,
                    'total_copies': 4,
                    'available_copies': 4
                },
                {
                    'title': 'Harry Potter and the Chamber of Secrets',
                    'description': "The second novel in the Harry Potter series.",
                    'author': rowling,
                    'category': fantasy,
                    'total_copies': 3,
                    'available_copies': 3
                },
                {
                    'title': 'The Hercule Poirot Collection',
                    'description': "A collection of Hercule Poirot mystery stories.",
                    'author': christie,
                    'category': mystery,
                    'total_copies': 2,
                    'available_copies': 2
                }
            ]
            
            for book_data in books_data:
                book, created = Book.objects.get_or_create(
                    title=book_data['title'],
                    defaults=book_data
                )
                if created:
                    self.stdout.write(f'Created book: {book.title}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('You can now:')
        self.stdout.write('1. Login to admin panel: admin/admin123')
        self.stdout.write('2. Test API with user: user/user123')
        self.stdout.write('3. Start the server with: python manage.py runserver')
