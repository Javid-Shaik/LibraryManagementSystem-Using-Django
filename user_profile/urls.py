from django.urls import path
from . import views

urlpatterns = [
    path('user_profile/<str:username>/', views.user_profile , name='user_profile'),
    path('edit_profile/' , views.edit_profile , name='edit_profile'),
    path('save_profile/<str:username>/',views.save_profile , name='save_profile'),
    path('borrow_books/<int:book_id>/' , views.borrow_books, name='borrow_books'),
    path('book_search/' , views.book_search , name='book_search'),
    path('learn_more/<int:book_id>/', views.learn_more , name='learn_more'),
    path('return_book/<int:book_id>/', views.return_book , name='return_book'),
    path('notify_book_available/<int:book_id>/', views.notify_book_available, name='notify_book_available'),
    path('subscribe/<str:username>/' , views.subscribe , name='subscribe'),
    path('subscription/<str:username>/' , views.subscription ,   name='subscription')
]