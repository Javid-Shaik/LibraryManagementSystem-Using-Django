# user_profile/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from my_app.models import Books, Borrowings

@shared_task
def send_book_available_notification(book_title, user_email):
    subject = 'Book Available Notification'
    message = f'The book "{book_title}" is now available in our library.'
    from_email = settings.DEFAULT_FROM_EMAIL
    print(from_email)
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
    
    
@shared_task
def send_overdue_reminders():
    overdue_books = Borrowings.objects.filter(due_date__lt=timezone.now(), status='Overdue')

    for book in overdue_books:
        subject = f"Reminder: Return Overdue Book - {book.book.title}"
        message = f"Dear {book.member.user.username},\n\nThis is a reminder to return the book '{book.book.title}' as soon as possible. It is currently overdue.\n\nThank you."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [book.member.user.email]
        print(subject , message , recipient_list)
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

@shared_task      
def send_upcoming_due_date_notifications():
    
    upcoming_books = Borrowings.objects.filter(due_date__lt=timezone.now()+timezone.timedelta(days=3) , status='Borrowed')
    
    for book in upcoming_books:
        subject = f"Upcoming Due Date: {book.title}"
        message = f"Dear {book.member.user.username},\n\nThis is a reminder that the book '{book.book.title}' is due in {book.due_date - timezone.now()} days.\n\nThank you."
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [book.borrower.email]
        print(subject , message , recipient_list)
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)
    

from .api import fetch_book_data, add_book_to_database

@shared_task
def fetch_and_add_book(isbn):
    book_data = fetch_book_data(isbn)
    if book_data:
        add_book_to_database(book_data)
