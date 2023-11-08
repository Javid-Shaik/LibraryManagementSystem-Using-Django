from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager ,PermissionsMixin
from datetime import date
from django.utils import timezone

class UserManager(BaseUserManager):
    
    def get_by_natural_key(self, username):
        return self.get(username=username)
    
    def create_user(self, email, username, password=None ):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None , **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        user = self.create_user(email, username, password)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return user

class RegisterModel(AbstractUser,PermissionsMixin):
    DEFAULT_USER_IMAGE = r'LibraryManagementSystem\\media\\profile\\default_user.jpg'
    ROLE_CHOICES = (
        ('student' , 'Student'),
        ('teacher', 'Teacher'),
        ('librarian' , 'Librarian'),
        ('admin', 'Admin')
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    role = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to="profile/", default=DEFAULT_USER_IMAGE ,null=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(max_length=200 ,blank=True, null=True)
    token = models.TextField(max_length=300 , blank=True, null = True)
    email_confirmed = models.BooleanField(default=False)
    
    
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
            if not self.id:
                # New instance, hash the password
                self.password = make_password(self.password)
            super().save(*args, **kwargs)
    
    USERNAME_FIELD = 'username'

    objects = UserManager()
    
    def has_module_perms(self, app_label):
        if self.is_superuser and app_label == 'my_app':
            return True
    
    def __str__(self):
        return "Username : "+self.username
    
class Books(models.Model):
    title = models.TextField(null=False)
    author_name = models.CharField(max_length=50)
    isbn = models.CharField(max_length=20)
    publisher = models.CharField(max_length=200,null=True,blank=True)
    publication = models.DateField()
    edition = models.IntegerField(null=True , blank=True)
    availability = models.CharField(max_length=10,default='No')
    cover_image = models.ImageField(upload_to="book_covers/")
    book_file = models.FileField(upload_to="books/",blank=True , null=True)
    copies_available = models.IntegerField(null=True,blank=True,default=2)
    description = models.TextField(max_length=2000 , null=True , blank=True)
    
    def __str__(self):
        return self.title

class Member(models.Model):
    user = models.OneToOneField(RegisterModel, on_delete=models.CASCADE)
    address = models.CharField(max_length=100 , blank=True , null=True)
    phone = models.CharField(max_length=15)
    borrowed_books = models.ManyToManyField(Books , through="borrowings")
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Members"



class Borrowings(models.Model):
    STATUS_CHOICES = (
        ('Borrowed', 'Borrowed'),
        ('Returned', 'Returned'),
        ('Overdue', 'Overdue'),
    )

    member = models.ForeignKey(Member , on_delete=models.CASCADE)
    book = models.ForeignKey(Books , on_delete=models.CASCADE)
    borrowed_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True , blank=True)
    fine_amount = models.DecimalField(max_digits=8, decimal_places=2, null=True,blank=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default="None")
    
    def __str__(self):
        return self.member.user.username+" "+self.book.title


    
    