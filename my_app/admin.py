from django.contrib import admin

# Register your models here.
from .models import RegisterModel , Books , Borrowings , Member
admin.site.register(RegisterModel)

admin.site.register(Books)
admin.site.register(Borrowings)
admin.site.register(Member)