# Electrical Parts Agency - Stock Management System

A comprehensive Django-based web application for managing electrical parts inventory, sales, and stock movements.

## 🚀 Features

- **Product Management**: Complete CRUD operations for products with categories, SKUs, and pricing
- **Stock Management**: Real-time stock tracking with low-stock alerts and movement history
- **Sales Management**: Customer management, sales processing, and analytics
- **Dashboard**: Comprehensive overview with KPIs and quick actions
- **Responsive UI**: Bootstrap 5 with modern, mobile-friendly design
- **Admin Panel**: Full Django admin integration
- **Data Visualization**: Charts and graphs for sales analytics
- **Automated Testing**: Comprehensive test suite with fake data generation

## 🛠️ Technology Stack

- **Backend**: Django 4.2.7
- **Database**: SQLite (development)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Charts**: Chart.js
- **Authentication**: Django built-in authentication
- **Image Handling**: Pillow
- **Fake Data**: Faker library
- **Documentation**: python-docx

## 📦 Installation

### Quick Setup

```bash
# Make setup script executable
chmod +x setup.sh

# Run automated setup
./setup.sh
```

### Manual Setup

```bash
# Install dependencies
pip install django pillow faker python-docx django-plotly-dash black

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Generate fake data
python manage.py generate_fake_data

# Collect static files
python manage.py collectstatic

# Start development server
python manage.py runserver
```

## 🎯 Usage

### Access Points

- **Main Dashboard**: http://localhost:8000/dashboard/
- **Admin Panel**: http://localhost:8000/admin/
- **Products**: http://localhost:8000/products/
- **Stock Management**: http://localhost:8000/stock/
- **Sales**: http://localhost:8000/sales/

### Default Credentials

- **Username**: admin
- **Password**: admin123

## 📊 Application Structure

```
electrical_parts_agency/
├── products_app/          # Product catalog management
├── stock_app/            # Stock level tracking and movements
├── sales_app/            # Sales processing and analytics
├── dashboard_app/        # Main dashboard
├── accounts_app/         # User authentication
├── templates/            # HTML templates
├── static/              # Static files (CSS, JS, images)
├── manage.py            # Django management script
├── setup.sh             # Automated setup script
├── test_app.py          # Test suite
└── generate_documentation.py  # Documentation generator
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python3 test_app.py
```

The test suite validates:
- Database models and relationships
- View accessibility
- Admin interface
- Data integrity
- Core functionality

## 📚 Documentation

Comprehensive documentation is available in `Electrical_Parts_Agency_Documentation.docx` including:

- System overview and architecture
- Feature descriptions
- Database schema
- API endpoints
- User guides
- Installation instructions
- Troubleshooting guide

## 🔧 Management Commands

### Generate Fake Data

```bash
python manage.py generate_fake_data --products 100 --sales 200
```

Options:
- `--categories`: Number of categories to create (default: 10)
- `--products`: Number of products to create (default: 50)
- `--customers`: Number of customers to create (default: 20)
- `--sales`: Number of sales to create (default: 100)

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Interface**: Clean, professional design with Bootstrap 5
- **Sidebar Navigation**: Easy access to all modules
- **Data Tables**: Sortable, searchable, and paginated
- **Alerts**: Low stock and system notifications
- **Charts**: Interactive data visualization
- **Quick Actions**: One-click access to common tasks

## 📈 Key Metrics

The dashboard displays:
- Total products and active products
- Stock levels and alerts
- Sales performance
- Revenue tracking
- Top-selling products
- Recent activity

## 🔒 Security Features

- Django's built-in authentication system
- CSRF protection
- SQL injection prevention
- XSS protection
- Secure file uploads
- User permission management

## 🚀 Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure media file storage
5. Set up SSL/HTTPS
6. Use production WSGI server (Gunicorn recommended)
7. Set up reverse proxy (Nginx recommended)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the documentation
- Review the troubleshooting guide
- Run the test suite to identify issues
- Check Django logs for error details

## 🎉 Success!

The Electrical Parts Agency Stock Management System is now ready for use! The application provides a complete solution for managing electrical parts inventory with a modern, responsive interface and comprehensive functionality.

---

**Happy Managing! 🔌⚡**
