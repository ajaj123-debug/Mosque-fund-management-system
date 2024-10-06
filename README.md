**Mosque Fund Management Dashboard**
**MosqueMate** is a web-based application built to help manage and track mosque donations, expenses, and overall financial savings. The dashboard is designed to offer a clear and detailed breakdown of total savings, monthly savings, deductions, and recent transactions. It also offers user role management and the ability to generate reports for better fund management.

**Table of Contents**

Project Overview
Features
Tech Stack
Installation
Configuration
Usage
Folder Structure
Contributing
License


**Project Overview**
The Mosque Fund Management Dashboard allows administrators and managers of mosques to easily view the mosque's financial details in a user-friendly dashboard. The dashboard is designed to offer:

An overview of total savings and expenses.
Month-wise saving and expense tracking.
Detailed transaction history.
Role-based access for users such as Admins and Managers to view and manage different areas of the dashboard.
Features


**Savings Overview:**
Displays total savings, current month’s savings, and previous month’s savings.

**Expense Tracking:**
Displays total deductions and a detailed list of current month's expenses.

**Transaction History:**
Shows recent transactions made to the mosque’s fund, including the donor's name, amount, and date.

**Reports Generation:**
Admins and Managers can generate user-based or monthly reports to review mosque financials in more detail.

**Role Management:**
Role selection for admin and manager with dynamic routing for different dashboard functionalities.

**Responsive Design:**
Fully responsive layout, works on mobile and web platforms.

**Tech Stack**
This project is built using the following technologies:

**Frontend:**
HTML5, CSS3 (inline styles)
JavaScript (for form actions and role management)
Responsive design for mobile and web

**Backend:**
Django (Python framework for managing data and routes)
Jinja2 for templating (for dynamic HTML generation)

**Database:**
SQLite (or any other Django-supported database)


**Installation**
Follow these steps to install and set up the project locally:


**Clone this repository:**
>>git clone https://github.com/ajaj123-debug/Mosque-fund-management-system.git

**Navigate to the project directory:**
>>cd mosque-fund-dashboard

**Create a virtual environment and activate it:**
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate


**Install the project dependencies:**

pip install -r requirements.txt


**Run the database migrations:**
>> python manage.py migrate


**Create a superuser (admin account):**
>> python manage.py createsuperuser

**Start the development server:**
python manage.py runserver
Access the application on:
http://127.0.0.1:8000


Configuration
Environment Variables
This project uses Django settings. You can configure the necessary environment variables in a .env file for database and other secret management.

Database Configuration
By default, the project uses SQLite.
To switch to another database like PostgreSQL, modify the DATABASES setting in settings.py and ensure the correct driver is installed in requirements.txt.
URLs
You can configure or add new routes in urls.py for new views or endpoints.

**Usage**

**Admin Panel:**
Access the Django admin panel by visiting /admin/ and logging in with the superuser credentials you created during setup.


**Role-Based Access:**
The dashboard contains role-based redirection for admins and managers. After selecting a role (Admin or Manager), the system will route the user to their respective section.

**Generating Reports:**
You can generate monthly or user-wise reports by navigating to the corresponding section in the dashboard.

**Manage Transactions:**
The system allows admins and managers to view, add, and update mosque savings and deductions directly through the dashboard.


**Folder Structure**

mosque-fund-dashboard/
│
├── mosque_fund/             # Main Django app
│   ├── migrations/          # Database migrations
│   ├── static/              # Static assets (CSS, JS, images)
│   ├── templates/           # HTML templates
│   ├── views.py             # Backend logic for routing
│   └── urls.py              # URL routing
├── manage.py                # Django management script
├── db.sqlite3               # Default SQLite database (auto-generated)
├── requirements.txt         # Python dependencies
└── README.md                # This file
Contributing
We welcome contributions! Here's how you can help:

Fork the project.
Create a new feature branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
This project is copyrighted to owner of this repo the me the **ajaj **
