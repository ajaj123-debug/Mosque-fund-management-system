from django.contrib import admin
from .models import Deduction, User, Transaction
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Deduction)
