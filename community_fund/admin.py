from django.contrib import admin
from .models import Deduction, User, Transaction
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Deduction)
admin.site.site_title = "Sunni Noori Jama Masjid"
admin.site.index_title = "Sunni Noori Jama Masjid"
admin.site.site_header = "Masjid Fund Itwa, Saran"
