from django.shortcuts import render , redirect , get_object_or_404
from my_app.models import RegisterModel , Member , Books , Borrowings
from django.contrib.auth.models import User

# from django.contrib import messages
from datetime import date, timedelta
from django.http import JsonResponse
from django.db.models import Q
from django.core.mail import send_mail

from .tasks import send_book_available_notification

from django.contrib.auth.decorators import login_required
# Create your views here.

#Functionality for diplaying the user profile.
@login_required
def user_profile(request , username ):
    try :
        member = Member.objects.get(user__username=username)
        borrowings = member.borrowings_set.all()
    except Member.DoesNotExist:
        # If Member object doesn't exist, create a new one
        
        # user = RegisterModel.objects.get(username=username)
        borrowings = None
        # member = Member.objects.create(user=user, address=user.address ,phone=user.phone)
        

    
    return render(request, 'profile/user_profile.html', {
        'user': request.user , 'borrowings' : borrowings
    })

#Functionality for providing the edit profile template
@login_required
def edit_profile(request):
    return render(request, 'profile/edit_profile.html',{
        'user':request.user
    })


#Fucntionality for saving the eidted profile of the user.
def save_profile(request , username):
    username = request.user.username
    profile = get_object_or_404(RegisterModel, username=username)
    if request.method == 'POST':
        
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        if fname :
            profile.first_name = fname
        if lname :
            profile.last_name = lname
        if address :
            profile.address = address  
        if image :
            profile.profile_image = image
        
        profile.email = email
        profile.phone = phone
        profile.save()
        
        return redirect('user_profile' , username=username)
    
    return render(request , 'profile/edit_profile.html')

# Functionality for borrowing the book
"""This function will check if the user has already borrowed the book or not 
    and also if the book is available or not. Based on the above two situations
    it will return response to the user using JsonResponse."""

@login_required
def borrow_books(request , book_id):
    user = request.user   
    book = Books.objects.get(id=book_id)
    user_exists_in_member_model = Member.objects.filter(user__username=user.username).exists()
    print(book.copies_available)
    already_borrowed = None
    
    if user_exists_in_member_model:
        member = Member.objects.get(user=user)
        already_borrowed = member.borrowed_books.filter(id=book_id).exists()
    else :
        return JsonResponse({'message': "Please subscribe to borrow the book", 'success': False , 'status':'non_subscriber'})
        # member = Member.objects.create(user=user , address = user.address , phone = user.phone )
    
    borrowed_date = date.today()
    due_date = borrowed_date + timedelta(days=14)
    
    if already_borrowed :
        status = Borrowings.objects.filter(book=book , member=member, status="Borrowed").exists()
        if status:
            message = f"The book {book.title} is already borrowed."
            return JsonResponse({'message': message, 'success': False , 'status':'borrowed'})
        
        message = f"You have successfully borrowed {book.title}"
        borrowing = Borrowings(
            book=book,
            member=member,
            borrowed_date=borrowed_date,
            due_date=due_date,
            status='Borrowed'
        )
        borrowing.save()
        book.copies_available -= 1
        if book.copies_available==0 :
            book.availability = 'No'
        book.save()
        return JsonResponse({'message': message, 'success': True , 'status':'now_borrowed'})
    
    elif book.availability == 'No' :
        message = f"The book {book.title} is currently not available."
        return JsonResponse({'message': message, 'success': False , 'status':'unavailable'})
    
    else:
        message = f"You have successfully borrowed {book.title}"
        borrowing = Borrowings(
            book=book,
            member=member,
            borrowed_date=borrowed_date,
            due_date=due_date,
            status='Borrowed'
        )
        borrowing.save()
        book.copies_available -= 1
        if book.copies_available==0 :
            book.availability = 'No'
        book.save()
        return JsonResponse({'message': message, 'success': True , 'status':'now_borrowed' })
    
#Fuctionality for searching the book

def book_search(request):
    book_domain = request.GET.get('book_domain')
    search_text = request.GET.get('text')
    books = None
    lookup = Q()
    if book_domain == 'All':
        lookup = Q(title__icontains=search_text) | Q(author_name__icontains=search_text) | Q(isbn__icontains=search_text) | Q(publisher__icontains=search_text)
    if book_domain == 'Title':
        lookup |= Q(title__icontains=search_text)
    elif book_domain == 'Author':
        lookup |= Q(author_name__icontains=search_text)
    elif book_domain == 'Isbn':
        lookup |= Q(isbn__icontains=search_text)
    elif book_domain == 'Publisher':
        lookup |= Q(publisher__icontains=search_text)
    books = Books.objects.filter(lookup)
    if books :
        return render(request , 'books/book_search.html', {
            'books' : books,
        # 'query' : lookup
        })
    else :
        return render(request, 'forms/homepage.html')

#Fucntionality for displaying the book information.
def learn_more(request,book_id):
    book = Books.objects.get(id=book_id)
    return render(request , 'books/learn_more.html', {
        'book': book
    })

@login_required
def return_book(request , book_id):
    user = request.user   
    book = Books.objects.get(id=book_id)
    member = Member.objects.get(user=user)
    borrowings = Borrowings.objects.filter(book=book.id , member=member)
    print(borrowings)
    return_date = date.today()
    if borrowings.exists():
        borrowing = borrowings.first()
        due_date = borrowing.due_date
    
        fine = 0 
        if return_date > due_date:
            fine = ((return_date-due_date).days)*5
    
        borrowing.status = "Returned"
        borrowing.fine_amount = fine
        borrowing.return_date = return_date
        borrowing.save()
        borrowing.delete()
        
        print(book.copies_available, book.title , member.user.username)
        book.copies_available = book.copies_available+1
        book.availability = "Yes"
        
        book.save()
    message = f"The book {book.title} is returned sucessfully"
    return redirect('user_profile' , username=user.username)
    
#Notification sending method

@login_required
def notify_book_available(request, book_id):
    user = request.user
    book = Books.objects.get(id=book_id)
    print(book)
    if book.availability:
        # Book is already available, send an immediate notification
        send_book_available_notification.delay(book.title, user.email)
        print(user.email)
        return JsonResponse({'message': f'You will receive an email when the book {book.title} becomes available.', 'success': True })
    else:
        # Book is not available, show the Notify button
        return JsonResponse({'message': 'The book is currently not available.', 'success': False })
    
def subscribe(request , username):
    return render(request , "profile/subscribe.html" , {
        'username':username
    })
    
def subscription(request , username):
    user = get_object_or_404(RegisterModel, username=username)
    member = Member.objects.create(user=user, address=user.address ,phone=user.phone)
    return redirect('signup:show_books')
    
    