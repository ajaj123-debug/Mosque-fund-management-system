from django.contrib import admin
from django.urls import path
from community_fund import views
from community_fund.views import *
from community_fund.views import monthwise_report
from community_fund.views import generate_report, add_transaction
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('home', views.home, name='home'),
    path('manager/login/', manager_login, name='manager_login'),
    path('add_deduction/', views.add_deduction, name='add_deduction'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('add_transaction/', views.add_transaction, name='add_transaction'),
    path('generate_user_report/', views.generate_user_report, name='generate_user_report'),
    path('monthwise-report/', monthwise_report, name='monthwise_report')
    
]