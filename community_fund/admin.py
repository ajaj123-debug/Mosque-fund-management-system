from django.contrib import admin
from .models import Deduction, User, Transaction
admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(Deduction)
admin.site.site_title = "Sunni Noori Jama Masjid"
admin.site.index_title = "Sunni Noori Jama Masjid"
admin.site.site_header = "Masjid Fund Itwa, Saran"

from django.contrib import admin
from .models import NamazTime

@admin.register(NamazTime)
class NamazTimeAdmin(admin.ModelAdmin):
    list_display = ('date', 'fajr_time', 'dhuhr_time', 'asr_time', 'maghrib_time', 'isha_time')
    list_filter = ('date',)
    search_fields = ('date',)

