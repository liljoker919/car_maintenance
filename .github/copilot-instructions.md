# Car Maintenance Tracker

Car Maintenance Tracker is a Django web application for managing vehicle information, registrations, insurance policies, and compliance tracking. The application uses Python 3.12+, Django 5.2+, SQLite database, and Bootstrap for the frontend.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Initial Setup
- Install Python dependencies:
  - `pip install Django` - Core framework (required)
  - `pip install black flake8` - Linting and formatting tools (recommended)
- Create static files directory: `mkdir -p static`
- Run database migrations: `python manage.py migrate` - takes 0.3-30 seconds
- NEVER CANCEL: Migration may take up to 30 seconds on slower systems. Set timeout to 60+ seconds.

### Development Workflow
- Bootstrap the application:
  - `cd /path/to/repository`
  - `pip install Django`
  - `mkdir -p static`
  - `python manage.py migrate`
- Run the development server: `python manage.py runserver 0.0.0.0:8000`
- Server starts in ~5 seconds and serves on http://localhost:8000
- Access admin interface at: http://localhost:8000/admin/ (requires superuser)
- Access login at: http://localhost:8000/auth/login/

### Testing
- Run full test suite: `python manage.py test` 
- NEVER CANCEL: Tests take 17-20 seconds (28 tests). Set timeout to 60+ seconds.
- All tests should pass - if any fail, investigate before making changes
- Tests cover models, views, templates, and form validation

### Code Quality
- Run linting: `flake8 . --exclude=migrations,venv,env,__pycache__ --max-line-length=88`
- NEVER CANCEL: Linting takes 0.2-2 seconds but set timeout to 30+ seconds.
- Run formatting check: `black --check . --exclude="migrations|venv|env|__pycache__"`
- Auto-format code: `black . --exclude="migrations|venv|env|__pycache__"`
- NEVER CANCEL: Formatting takes 0.5-2 seconds but set timeout to 30+ seconds.

## Validation

### Manual Testing Scenarios
ALWAYS run through these scenarios after making changes:
1. **User Registration/Login Flow:**
   - Visit homepage at http://localhost:8000
   - Navigate to Register page
   - Create new user account
   - Login with created credentials
   - Verify redirect to vehicles list

2. **Vehicle Management Flow:**
   - Login as user
   - Navigate to "My Garage" 
   - Add a new vehicle with all required fields (make, model, year, mileage)
   - Edit vehicle information
   - Verify vehicle appears in list with correct data

3. **Admin Interface Flow:**
   - Create superuser: `python manage.py createsuperuser --username admin --email admin@test.com --noinput`
   - Set password: `echo "from django.contrib.auth.models import User; user = User.objects.get(username='admin'); user.set_password('admin123'); user.save()" | python manage.py shell`
   - Login to admin at http://localhost:8000/admin/
   - Verify all models (Vehicle, CarRegistration, InsurancePolicy) are accessible

### Testing Requirements
- Run `python manage.py test` before committing changes
- All 28 tests must pass
- Run `flake8` to check code style compliance
- Use `black` to format code consistently

## Application Structure

### Django Apps
- **vehicles**: Core vehicle management (models: Vehicle)
- **compliance**: Registration and inspection tracking (models: CarRegistration)  
- **insurance**: Insurance policy management (models: InsurancePolicy)
- **registration**: User registration and authentication

### Key Files and Directories
- `manage.py`: Django management script (run with `python manage.py <command>`)
- `car_maintenance/settings.py`: Main configuration file
- `car_maintenance/urls.py`: URL routing configuration
- `templates/`: HTML templates with Bootstrap styling
- `static/`: Static files directory (CSS, JS, images)
- `*/migrations/`: Database migration files (do not modify directly)
- `*/tests.py`: Test files for each app

### Database
- Uses SQLite (`db.sqlite3`) for development
- Database file created automatically on first migration
- Test database created/destroyed automatically during testing

## Common Tasks

### Adding New Features
1. Create/modify models in appropriate app
2. Generate migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Update views, templates, and URLs as needed
5. Write tests for new functionality
6. Run full test suite to ensure no regressions

### Debugging
- Check Django logs in console when running development server
- Use `python manage.py shell` for interactive Django shell
- Use `python manage.py dbshell` for database access
- Enable DEBUG=True in settings.py for detailed error pages

### User Management
- Create superuser: `python manage.py createsuperuser`
- Create regular user via registration form or admin interface
- Users are automatically redirected to `/vehicles/` after login

### Performance Notes
- **NEVER CANCEL** any of these operations:
  - Database migrations: 0.3-30 seconds (set timeout: 60+ seconds)
  - Test suite: 17-20 seconds for 28 tests (set timeout: 60+ seconds)  
  - Linting: 0.2-2 seconds (set timeout: 30+ seconds)
  - Development server startup: 3-8 seconds (set timeout: 30+ seconds)
  - Code formatting: 0.5-2 seconds (set timeout: 30+ seconds)

## Repository Structure

```
.
├── car_maintenance/          # Main Django project
│   ├── settings.py          # Django configuration
│   ├── urls.py             # URL routing
│   ├── views.py            # Project-level views
│   └── wsgi.py             # WSGI configuration
├── vehicles/               # Vehicle management app
│   ├── models.py           # Vehicle model
│   ├── views.py            # Vehicle views
│   ├── forms.py            # Vehicle forms
│   ├── tests.py            # Vehicle tests
│   └── fixtures/           # Test data fixtures
├── compliance/             # Registration/compliance app
│   ├── models.py           # CarRegistration model
│   ├── views.py            # Compliance views
│   ├── templatetags/       # Custom template filters
│   └── tests.py            # Compliance tests
├── insurance/              # Insurance management app
│   ├── models.py           # InsurancePolicy model
│   ├── views.py            # Insurance views
│   └── tests.py            # Insurance tests
├── registration/           # User registration app
├── templates/              # HTML templates
│   ├── base.html           # Base template with Bootstrap
│   └── home.html           # Homepage template
├── static/                 # Static files (CSS, JS, images)
├── manage.py               # Django management script
└── db.sqlite3              # SQLite database (created after migration)
```

## Command Reference

### Essential Commands (Copy-Paste Ready)
```bash
# Setup and run application
pip install Django
mkdir -p static
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# Testing and quality
python manage.py test
flake8 . --exclude=migrations,venv,env,__pycache__ --max-line-length=88
black --check . --exclude="migrations|venv|env|__pycache__"

# User management
python manage.py createsuperuser
python manage.py shell

# Development
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

### URLs for Testing
- Homepage: http://localhost:8000/
- Login: http://localhost:8000/auth/login/
- Register: http://localhost:8000/register/
- Vehicles: http://localhost:8000/vehicles/
- Admin: http://localhost:8000/admin/

All commands have been validated to work correctly. The application builds successfully, all tests pass, and the development server runs without issues.