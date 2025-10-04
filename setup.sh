#!/bin/bash

echo "=========================================="
echo "Electrical Parts Agency - Setup Script"
echo "=========================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

echo "Installing required packages..."
pip3 install django pillow faker python-docx django-plotly-dash black

echo "Running database migrations..."
python3 manage.py makemigrations --skip-checks
python3 manage.py migrate

echo "Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python3 manage.py shell

echo "Generating fake data..."
python3 manage.py generate_fake_data

echo "Collecting static files..."
python3 manage.py collectstatic --noinput

echo "Running tests..."
python3 test_app.py

echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "To start the development server, run:"
echo "python3 manage.py runserver"
echo ""
echo "Then visit:"
echo "- Admin panel: http://localhost:8000/admin/"
echo "- Main dashboard: http://localhost:8000/dashboard/"
echo ""
echo "Login credentials:"
echo "Username: admin"
echo "Password: admin123"
echo "=========================================="
