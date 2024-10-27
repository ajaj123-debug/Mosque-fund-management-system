from django.db import models
from django.utils import timezone
from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=100)
    joined_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)
    # is_collected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.amount}"


class Deduction(models.Model):
    CATEGORY_CHOICES = [
        ('इमाम साहब की सैलरी में', 'इमाम साहब की सैलरी में'),
        ('मस्जिद में खर्च', 'मस्जिद में खर्च'),
        ('बिजली/बल्ब/तार/पंखा', 'बिजली/बल्ब/तार/पंखा'),
        ('साउंड सिस्टम', 'साउंड सिस्टम'),
        ('ईद में सजावट', 'ईद में सजावट'),
        ('कुर्बानी में सजावट', 'कुर्बानी में सजावट'),
        ('चापाकल', 'चापाकल'),
        ('वाइपर खरीदने में', 'वाइपर खरीदने में'),
        ('झाड़ू', 'झाड़ू'),
        ('ताला/चाबी', 'ताला/चाबी'),
        ('लोटा', 'लोटा'),
        ('पेंटिंग', 'पेंटिंग'),
        ('ईंट', 'ईंट'),
        ('गिट्टी', 'गिट्टी'),
        ('बालू', 'बालू'),
        ('सीमेंट', 'सीमेंट'),
        ('छड़', 'छड़'),
        ('मिस्त्री/लेबर', 'मिस्त्री/लेबर'),
        ('टाइल्स', 'टाइल्स'),
    ]
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.category} - {self.amount} on {self.date}"




from django.db import models

class NamazTime(models.Model):
    date = models.DateField()
    fajr_time = models.TimeField()
    dhuhr_time = models.TimeField()
    asr_time = models.TimeField()
    maghrib_time = models.TimeField()
    isha_time = models.TimeField()

    def __str__(self):
        return f"Namaz Times for {self.date}"
