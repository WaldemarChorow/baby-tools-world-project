# Development Guide

This guide provides detailed information for developers working on the Baby Tools World project.

## Code Standards and Quality

### PEP 8 Compliance

The project follows PEP 8, the Python Enhancement Proposal for code style, with the following specific requirements:

- **Class Names**: Use PascalCase (e.g., `Category`, `Product`, `Tag`)
- **Function and Variable Names**: Use snake_case (e.g., `product_list`, `category_slug`)
- **Line Length**: Maximum 120 characters per line (enforced by Flake8)

### Type Hints

All new functions and significant variables must include type hints for better code clarity and IDE support:

```python
from typing import Optional
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet

def product_detail(request: HttpRequest, category_slug: str, pk: int) -> HttpResponse:
    """Display detailed information about a specific product."""
    related_products: QuerySet[Product] = Product.objects.filter(category=product.category)
    initial: dict = {}
    existing: Optional[Comment] = product.comments.filter(user=request.user).first()
```

### DocStrings

All functions and classes must include docstrings that describe their purpose, parameters, and return values:

```python
def product_list(
    request: HttpRequest, category_slug: Optional[str] = None
) -> HttpResponse:
    """Display list of all products, optionally filtered by category.

    Args:
        request: The HTTP request object
        category_slug: Optional slug for filtering products by category

    Returns:
        HttpResponse: Rendered products.html template with categories and products
    """
```

### Code Formatting

The project uses two code formatters to maintain consistent style:

#### Black

Black is an opinionated code formatter that ensures consistent code style.

```bash
# Format all Python files in the current directory
black .

# Format a specific directory
black products/
```

#### Flake8

Flake8 is a linting tool that checks for PEP 8 violations and other code quality issues.

```bash
# Check all Python files for style violations
flake8 .

# Check a specific directory with custom settings
flake8 products/ --max-line-length=120
```

#### isort

isort ensures that imports are sorted and organized correctly.

```bash
# Sort imports in all Python files
isort .

# Sort imports in a specific directory
isort products/
```

## Git Workflow

### Branch Naming

Use descriptive branch names that indicate the feature or fix being implemented:

- Feature branches: `feature/add-product-tags`, `feature/user-dashboard`
- Bug fix branches: `bugfix/fix-comment-form`, `bugfix/empty-products-list`
- Hotfix branches: `hotfix/critical-bug-fix`

### Commit Messages

Write clear and descriptive commit messages that explain what changes were made and why:

```
Add type hints and docstrings for PEP 8 compliance

- Add type hints to function parameters and return types
- Add type hints to variables in views.py
- Add comprehensive docstrings to functions and classes
- Improve code documentation for better maintainability
```

### Pull Requests

When creating a pull request:

1. Provide a clear description of the changes
2. Reference any related issues
3. Ensure all CI/CD checks pass
4. Request review from team members
5. Merge only after approval

## Testing

### Running Tests

Execute tests using the Django test runner:

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test products

# Run tests for a specific test class
python manage.py test products.tests.TestProductModel

# Run tests with verbosity
python manage.py test --verbosity=2
```

### Writing Tests

Create test files in the `tests` module within each app:

```python
from django.test import TestCase
from products.models import Product, Tag, Category

class ProductModelTestCase(TestCase):
    """Test cases for the Product model."""

    def setUp(self) -> None:
        """Set up test data."""
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.tag = Tag.objects.create(name="Bestseller")

    def test_product_creation(self) -> None:
        """Test that a product can be created successfully."""
        product = Product.objects.create(
            name="Test Product",
            price=99.99,
            category=self.category,
        )
        product.tags.add(self.tag)

        self.assertEqual(product.name, "Test Product")
        self.assertIn(self.tag, product.tags.all())
```

## Environment Configuration

### Development Environment

For development, copy and configure the example environment file:

```bash
# Copy the example file
cp example.env src/.env

# Edit the .env file with development settings
# ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
# DEBUG=True
```

### Production Environment

For production deployments, ensure:

```
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
SECRET_KEY=<strong-random-key>
```

## Database Operations

### Creating Migrations

When modifying models, create and apply migrations:

```bash
# Create a migration for model changes
python manage.py makemigrations

# Apply migrations to the database
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

### Seeding Data

Populate the database with initial data:

```bash
# Run the seed_db management command
python manage.py seed_db
```

## Docker Development

### Building the Image

```bash
docker build -t baby-tools-world:dev .
```

### Running in Development Mode

```bash
docker run --rm -it -p 8000:8000 -v $(pwd)/src:/app/src baby-tools-world:dev
```

This command mounts the local `src` directory into the container, allowing you to edit code and see changes immediately.

### Running Tests in Docker

```bash
docker run --rm baby-tools-world:dev python manage.py test
```

## Debugging

### Django Debug Toolbar

The project can be extended with Django Debug Toolbar for development. Install it with:

```bash
pip install django-debug-toolbar
```

Then add it to `INSTALLED_APPS` in your settings and configure it in your `urls.py`.

### Python Debugger

Use the Python debugger for step-by-step execution:

```python
import pdb

def product_detail(request):
    pdb.set_trace()  # Execution will pause here
    # Debug your code
```

## Documentation

All documentation should be written in English using complete sentences. Key documentation locations:

- **Main Documentation**: `README.md` - Overview and quickstart
- **Feature Documentation**: `docs/product-tags.md` - Detailed feature information
- **Development Guide**: `docs/development.md` - This file
- **Code Comments**: Inline comments in Python code explain complex logic
- **DocStrings**: Function and class docstrings describe usage and parameters

## Useful Django Management Commands

```bash
# Interactive Python shell with Django context
python manage.py shell

# Create a superuser account
python manage.py createsuperuser

# Change a user's password
python manage.py changepassword <username>

# Collect static files for production
python manage.py collectstatic

# Check for any issues in the project
python manage.py check

# Show all available management commands
python manage.py help
```
