from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'signup'
urlpatterns = [
    path("login", views.login_user , name="login_user"),
    path("register" , views.register , name = "register"),
    path("details", views.details , name="details"),
    path("",views.homepage, name="homepage"),
    path("logout_user",views.logout_user, name="logout"),
    path('show_books', views.show_books , name='show_books'),
    path('featured_books' , views.featured_books , name='featured_books'),
    path('about_libraquest'  , views.about_libraquest , name='about_libraquest'),
    path('confirm/<str:uidb64>/<str:token>/', views.confirm_email, name='confirm_email'),
    path('forgot_password/' , views.forgot_password , name='forgot_password'),
    path('reset_password/' , views.reset_password , name='reset_password'),
    path('reset_password_confirm/<str:uidb64>/<str:token>/', views.reset_password_confirm, name='reset_password_confirm'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
