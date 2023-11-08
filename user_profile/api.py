# books/api.py
import requests

def fetch_book_data(isbn):
    api_key = 'YOUR_API_KEY'
    url = f'https://api.example.com/books/{isbn}?apikey={api_key}'

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def add_book_to_database(book_data):
    from .models import Books  # Import your Book model
    book = Books( title = ['title'],
        author_name = ['author'],
        isbn = ['isbn'],
        publisher = ['publisher'],
        publication = ['publication'],
        edition = ['availability'],
        availability = ['avialability'],
        cover_image = ['cover_image'],
        book_file = ['book_filr'],
        copies_available = ['copies_available'],
        description = ['descrtion'],
        )
    book.save()
