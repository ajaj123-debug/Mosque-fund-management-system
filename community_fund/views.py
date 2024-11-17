import io,datetime
from weasyprint import HTML
from calendar import monthrange
from django.db.models import Sum
from django.utils import timezone
from .forms import UserReportForm
from django.contrib import messages
from django.http import HttpResponse
from .models import Transaction, Deduction
from PIL import Image, ImageDraw, ImageFont
from django.shortcuts import render, redirect
from django.template.loader import get_template
from .forms import TransactionForm, DeductionForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required









normal_users = {
    "Abbas", "Mumtaj", "Nasir", "Ahsan", "Safik", "Imteyaj",
    "Manjur", "Sultan", "Makbul", "Liyakat", "Yunus",
    "Muslim", "Mustakim", "Barkat", "Abdul Hasan", "Shamsad",
    "Aslam", "Wajif", "Azad", "Israel", "Kamal", "Itwa",
    "Haidar", "Najrul", "Arman", "Shakeel", "Hanif",
    "Afzal","Faruk","Shahid","Asgar","Ajaj", "Rashid", "Ashif",
    "Washim","Sarfaraz","Danish","Raja","Abid","Hajir","Sabiha","Sulman","Lie"
}



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username in normal_users and password == '123': 
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Username : Itwa Password : 123'})
    return render(request, 'login.html')











def home(request):
    now = timezone.now()
    total_savings = Transaction.objects.aggregate(total=Sum('amount'))['total'] or 0
    # Get deductions for the current month
    current_month_deductions = Deduction.objects.filter(
        date__year=now.year,
        date__month=now.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    # Get total deductions
    total_deductions = Deduction.objects.aggregate(total=Sum('amount'))['total'] or 0
    # Calculate savings after deduction
    net_total_savings = total_savings - total_deductions
    current_month_savings = Transaction.objects.filter(
        date__year=now.year,
        date__month=now.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    # Calculate first and last day of the current month
    first_day_of_current_month = datetime.date(current_year, current_month, 1)
    last_day_of_current_month = datetime.date(current_year, current_month, monthrange(current_year, current_month)[1])

    # Calculate first and last day of the previous month
    first_day_of_previous_month = datetime.date(current_year, current_month - 1, 1) if current_month > 1 else datetime.date(current_year - 1, 12, 1)
    # last_day_of_previous_month = datetime.date(current_year, current_month, 1) - datetime.timedelta(days=1)
    last_day_of_previous_month = timezone.make_aware(datetime.datetime(current_year, current_month, 1) - datetime.timedelta(days=1))
    
    
    # Fetch transactions and deductions for the current month
    current_month_transactions = Transaction.objects.filter(date__range=[first_day_of_current_month, now])
    # current_month_deductions = Deduction.objects.filter(date__range=[first_day_of_current_month, now])

    # Apply current month deductions
    current_month_savings_after_deduction = current_month_savings - current_month_deductions
    # Get recent transactions
    recent_transactions = Transaction.objects.order_by('-date')[:15]
    # Fetch transactions and deductions for the previous month
    previous_month_transactions = Transaction.objects.filter(date__range=[first_day_of_previous_month, last_day_of_previous_month])
    previous_month_deductions = Deduction.objects.filter(date__range=[first_day_of_previous_month, last_day_of_previous_month])

    # Calculate totals for previous month
    total_income_previous = previous_month_transactions.aggregate(total=Sum('amount'))['total'] or 0
    total_deductions_previous = previous_month_deductions.aggregate(total=Sum('amount'))['total'] or 0
    total_savings_previous = total_income_previous - total_deductions_previous
    context = {
        'total_savings': net_total_savings,
        'current_month_savings': current_month_savings_after_deduction,
        'current_month_deductions': current_month_deductions,  # Current month deductions
        'total_deductions': total_deductions,  # Total deductions till now
        'recent_transactions': recent_transactions,
        'deductions': Deduction.objects.all(),  # Fetch all deductions to display in the template
        'total_savings_previous': total_savings_previous,
    }
    return render(request, 'home.html', context)







@login_required
def add_transaction (request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        deduction_form = DeductionForm(request.POST)
        
        # Handle transaction form
        if form.is_valid():
            form.save()
            return redirect('add_transaction')

        # Handle deduction form
        if deduction_form.is_valid():
            deduction_form.save()
            messages.success(request, 'Deduction added successfully!')
            return redirect('home')
            # return redirect('add_transaction')
    else:
        form = TransactionForm()
        deduction_form = DeductionForm()

    return render(request, 'add_transaction.html', {
        'form': form,
        'deduction_form': deduction_form
    })
    
    
    
    
    
    


def add_deduction(request):
    if request.method == 'POST':
        form = DeductionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = DeductionForm()
    return render(request, 'add_deduction.html', {'form': form})








def generate_report(request):
    format = request.GET.get('format', 'pdf')  # Default to PDF
    
    # Get the current time in UTC and convert to local timezone
    now = timezone.now()

    # Ensure datetime is timezone-aware before using localtime
    if timezone.is_naive(now):
        now = timezone.make_aware(now)

    now = timezone.localtime(now)  # Convert to the local timezone (Asia/Kolkata)

    # Get first and last date of the current month
    first_day_of_month = timezone.localtime(
        timezone.make_aware(datetime.datetime(now.year, now.month, 1))
    )
    last_day_of_month = timezone.localtime(
        timezone.make_aware(
            datetime.datetime(now.year, now.month, monthrange(now.year, now.month)[1])
        )
    )
    # Fetch transactions for the current month
    transactions = Transaction.objects.filter(date__range=[first_day_of_month, now])

    # Calculate total income, expenditure, and savings
    total_income = transactions.aggregate(total=Sum('amount'))['total'] or 0
    total_deductions = Deduction.objects.filter(date__range=[first_day_of_month, now]).aggregate(total=Sum('amount'))['total'] or 0
    total_savings = total_income - total_deductions

    # Prepare data for the report
    context = {
        'month_name': now.strftime('%B'),
        'transactions': transactions,
        'total_income': total_income,
        'total_deductions': total_deductions,
        'total_savings': total_savings,
        'generation_time': now.strftime('%Y-%m-%d %H:%M:%S'),  # Add generation time
    }

    if format == 'pdf':
        return generate_pdf_report(context)
    elif format == 'png':
        return generate_png_report(context)








def generate_pdf_report(context):
    # Render HTML template
    template = get_template('report_template.html')  # Use your HTML template for the PDF
    html = template.render(context)

    # Create PDF using WeasyPrint
    pdf = HTML(string=html).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report_{}.pdf"'.format(context['month_name'])
    return response








def generate_png_report(context):
    # Create a blank image for PNG (width, height)
    img = Image.new('RGB', (1000, 1400), color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    # Basic font setup
    font = ImageFont.truetype("arial.ttf", 20)

    # Draw report title
    d.text((10, 10), "Report for " + context['month_name'], fill=(0, 0, 0), font=font)

    # Add serial number, name, and amount columns
    y_position = 80
    for idx, transaction in enumerate(context['transactions'], start=1):
        d.text((8, y_position), f"{idx}. {transaction.user.name}", fill=(0, 0, 0), font=font)
        d.text((400, y_position), f"₹{transaction.amount}", fill=(0, 0, 0), font=font)
        y_position += 30

    # Add totals at the bottom
    y_position += 100
    d.text((10, y_position), f"Total Income: ₹{context['total_income']}", fill=(0, 0, 0), font=font)
    y_position += 50
    d.text((10, y_position), f"Total Deductions: ₹{context['total_deductions']}", fill=(0, 0, 0), font=font)
    y_position += 50
    d.text((10, y_position), f"Total Savings: ₹{context['total_savings']}", fill=(0, 0, 0), font=font)

    # Save the image to a byte stream
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="image/png")
    response['Content-Disposition'] = 'attachment; filename="report_{}.png"'.format(context['month_name'])
    return response








def generate_user_report(request):
    if request.method == 'POST':
        form = UserReportForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')

            # Fetch transactions based on user and date range
            filters = {}
            if user:
                filters['user'] = user
            if start_date:
                filters['date__gte'] = start_date
            if end_date:
                filters['date__lte'] = end_date

            transactions = Transaction.objects.filter(**filters)

            # Calculate totals
            total_income = transactions.aggregate(total=Sum('amount'))['total'] or 0

            context = {
                'transactions': transactions,
                'total_income': total_income,
                'user': user.name if user else 'All Users',
                'start_date': start_date,
                'end_date': end_date,
            }
            return render(request, 'user_report.html', context)
    else:
        form = UserReportForm()

    return render(request, 'generate_user_report.html', {'form': form})








from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

def manager_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_authenticated and user.is_staff:  # Assuming managers are staff
            login(request, user)
            # Redirect to the 'next' parameter if it exists, else default to 'add_transaction'
            next_url = request.POST.get('next', 'add_transaction')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'manager_login.html')









def monthwise_report(request):
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    # Calculate first and last day of the current month
    first_day_of_current_month = datetime.date(current_year, current_month, 1)
    last_day_of_current_month = datetime.date(current_year, current_month, monthrange(current_year, current_month)[1])

    # Calculate first and last day of the previous month
    first_day_of_previous_month = datetime.date(current_year, current_month - 1, 1) if current_month > 1 else datetime.date(current_year - 1, 12, 1)
    last_day_of_previous_month = datetime.date(current_year, current_month, 1) - datetime.timedelta(days=1)

    # Fetch transactions and deductions for the current month
    current_month_transactions = Transaction.objects.filter(date__range=[first_day_of_current_month, now])
    current_month_deductions = Deduction.objects.filter(date__range=[first_day_of_current_month, now])

    # Fetch transactions and deductions for the previous month
    previous_month_transactions = Transaction.objects.filter(date__range=[first_day_of_previous_month, last_day_of_previous_month])
    previous_month_deductions = Deduction.objects.filter(date__range=[first_day_of_previous_month, last_day_of_previous_month])

    # Calculate totals for current month
    total_income_current = current_month_transactions.aggregate(total=Sum('amount'))['total'] or 0
    total_deductions_current = current_month_deductions.aggregate(total=Sum('amount'))['total'] or 0
    total_savings_current = total_income_current - total_deductions_current

    # Calculate totals for previous month
    total_income_previous = previous_month_transactions.aggregate(total=Sum('amount'))['total'] or 0
    total_deductions_previous = previous_month_deductions.aggregate(total=Sum('amount'))['total'] or 0
    total_savings_previous = total_income_previous - total_deductions_previous

    # Check if there is data for the previous month
    previous_month_data_available = previous_month_transactions.exists() or previous_month_deductions.exists()

    context = {
        'current_month_transactions': current_month_transactions,
        'current_month_deductions': current_month_deductions,
        'total_income_current': total_income_current,
        'total_deductions_current': total_deductions_current,
        'total_savings_current': total_savings_current,
        'previous_month_transactions': previous_month_transactions,
        'previous_month_deductions': previous_month_deductions,
        'total_income_previous': total_income_previous,
        'total_deductions_previous': total_deductions_previous,
        'total_savings_previous': total_savings_previous,
        'current_month_name': now.strftime('%B'),
        'previous_month_name': (now - datetime.timedelta(days=30)).strftime('%B'),  # Approximate for month name
        'year': current_year,
        'previous_month_data_available': previous_month_data_available,
    }

    return render(request, 'monthwise_report.html', context)




def index(request):
    now = timezone.now()
    total_savings = Transaction.objects.aggregate(total=Sum('amount'))['total'] or 0
    # Get deductions for the current month
    current_month_deductions = Deduction.objects.filter(
        date__year=now.year,
        date__month=now.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    # Get total deductions
    total_deductions = Deduction.objects.aggregate(total=Sum('amount'))['total'] or 0
    # Calculate savings after deduction
    net_total_savings = total_savings - total_deductions
    current_month_savings = Transaction.objects.filter(
        date__year=now.year,
        date__month=now.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    # Calculate first and last day of the current month
    first_day_of_current_month = datetime.date(current_year, current_month, 1)
    last_day_of_current_month = datetime.date(current_year, current_month, monthrange(current_year, current_month)[1])

    # Calculate first and last day of the previous month
    first_day_of_previous_month = datetime.date(current_year, current_month - 1, 1) if current_month > 1 else datetime.date(current_year - 1, 12, 1)
    # last_day_of_previous_month = datetime.date(current_year, current_month, 1) - datetime.timedelta(days=1)
    last_day_of_previous_month = timezone.make_aware(datetime.datetime(current_year, current_month, 1) - datetime.timedelta(days=1))
    
    
    # Fetch transactions and deductions for the current month
    current_month_transactions = Transaction.objects.filter(date__range=[first_day_of_current_month, now])
    # current_month_deductions = Deduction.objects.filter(date__range=[first_day_of_current_month, now])

    # Apply current month deductions
    current_month_savings_after_deduction = current_month_savings - current_month_deductions
    # Get recent transactions
    recent_transactions = Transaction.objects.order_by('-date')[:15]
    # Fetch transactions and deductions for the previous month
    previous_month_transactions = Transaction.objects.filter(date__range=[first_day_of_previous_month, last_day_of_previous_month])
    previous_month_deductions = Deduction.objects.filter(date__range=[first_day_of_previous_month, last_day_of_previous_month])

    # Calculate totals for previous month
    total_income_previous = previous_month_transactions.aggregate(total=Sum('amount'))['total'] or 0
    total_deductions_previous = previous_month_deductions.aggregate(total=Sum('amount'))['total'] or 0
    total_savings_previous = total_income_previous - total_deductions_previous
    context = {
        'total_savings': net_total_savings,
        'current_month_savings': current_month_savings_after_deduction,
        'current_month_deductions': current_month_deductions,  # Current month deductions
        'total_deductions': total_deductions,  # Total deductions till now
        'recent_transactions': recent_transactions,
        'deductions': Deduction.objects.all(),  # Fetch all deductions to display in the template
        'total_savings_previous': total_savings_previous,
    }
    return render(request, 'index.html', context)

def my_view(request):
    if request.method == 'HEAD':
        # Return an empty response with just headers
        return HttpResponse(status=200)
    # Handle other methods as usual
    
    
    
    
    
    
    from django.shortcuts import render
from .models import NamazTime
from datetime import date

def namaz_times_view(request):
    today = date.today()
    namaz_times = NamazTime.objects.filter(date=today).first()  # Fetch today's namaz times

    context = {
        'namaz_times': namaz_times,
    }
    return render(request, 'namaz_times.html', context)









def index(request):
    now = timezone.now()
    total_savings = Transaction.objects.aggregate(total=Sum('amount'))['total'] or 0
    # Get deductions for the current month
    current_month_deductions = Deduction.objects.filter(
        date__year=now.year,
        date__month=now.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    # Get total deductions
    total_deductions = Deduction.objects.aggregate(total=Sum('amount'))['total'] or 0
    # Calculate savings after deduction
    net_total_savings = total_savings - total_deductions
    current_month_savings = Transaction.objects.filter(
        date__year=now.year,
        date__month=now.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    now = timezone.now()
    current_month = now.month
    current_year = now.year

    # Calculate first and last day of the current month
    first_day_of_current_month = datetime.date(current_year, current_month, 1)
    last_day_of_current_month = datetime.date(current_year, current_month, monthrange(current_year, current_month)[1])

    # Calculate first and last day of the previous month
    first_day_of_previous_month = datetime.date(current_year, current_month - 1, 1) if current_month > 1 else datetime.date(current_year - 1, 12, 1)
    # last_day_of_previous_month = datetime.date(current_year, current_month, 1) - datetime.timedelta(days=1)
    last_day_of_previous_month = timezone.make_aware(datetime.datetime(current_year, current_month, 1) - datetime.timedelta(days=1))
    
    
    # Fetch transactions and deductions for the current month
    current_month_transactions = Transaction.objects.filter(date__range=[first_day_of_current_month, now])
    # current_month_deductions = Deduction.objects.filter(date__range=[first_day_of_current_month, now])

    # Apply current month deductions
    current_month_savings_after_deduction = current_month_savings - current_month_deductions
    # Get recent transactions
    recent_transactions = Transaction.objects.order_by('-date')[:15]
    # Fetch transactions and deductions for the previous month
    previous_month_transactions = Transaction.objects.filter(date__range=[first_day_of_previous_month, last_day_of_previous_month])
    previous_month_deductions = Deduction.objects.filter(date__range=[first_day_of_previous_month, last_day_of_previous_month])

    # Calculate totals for previous month
    total_income_previous = previous_month_transactions.aggregate(total=Sum('amount'))['total'] or 0
    total_deductions_previous = previous_month_deductions.aggregate(total=Sum('amount'))['total'] or 0
    total_savings_previous = total_income_previous - total_deductions_previous
    context = {
        'total_savings': net_total_savings,
        'current_month_savings': current_month_savings_after_deduction,
        'current_month_deductions': current_month_deductions,  # Current month deductions
        'total_deductions': total_deductions,  # Total deductions till now
        'recent_transactions': recent_transactions,
        'deductions': Deduction.objects.all(),  # Fetch all deductions to display in the template
        'total_savings_previous': total_savings_previous,
    }
    return render(request, 'index.html', context)