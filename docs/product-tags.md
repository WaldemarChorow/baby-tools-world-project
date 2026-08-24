# Product Tags Feature Documentation

## Overview

The Product Tags feature provides a flexible tagging system that allows products to be labeled with multiple tags for better organization and filtering. Tags can be managed through the Django admin interface and are displayed on product detail pages.

## Features

- **Multiple Tags per Product**: Each product can be associated with multiple tags through a many-to-many relationship.
- **Admin Management**: Tags can be created, edited, and deleted through the Django admin interface.
- **Product Filtering**: Products can be filtered by tags in the admin interface for easier management.
- **Frontend Display**: Product tags are displayed as badges on the product detail page, with a fallback message when no tags are present.
- **Search and Sort**: Tags can be searched by name in the admin interface for quick access.

## Database Schema

### Tag Model

The `Tag` model represents a product tag with the following fields:

- `name` (CharField): Unique name of the tag, maximum 100 characters.
- `created_at` (DateTimeField): Automatically set timestamp when the tag is created.
- `updated_at` (DateTimeField): Automatically updated timestamp when the tag is modified.

### Product-Tag Relationship

The `Product` model contains a many-to-many field that relates products to tags:

```python
tags = models.ManyToManyField(
    Tag,
    related_name="products",
    blank=True,
    help_text="Tags are assigned to products here.",
)
```

This relationship allows:
- Access all tags for a product: `product.tags.all()`
- Access all products for a tag: `tag.products.all()`

## Usage

### Creating Tags in the Admin Interface

1. Log in to the Django admin interface at `/admin/`
2. Navigate to the "Tags" section
3. Click "Add Tag" to create a new tag
4. Enter the tag name and click "Save"

### Assigning Tags to Products

1. Navigate to the Products section in the admin interface
2. Select a product to edit
3. In the product edit form, find the "Tags" field
4. Select one or more tags from the available options
5. Click "Save" to update the product

### Filtering Products by Tag

1. Navigate to the Products section in the admin interface
2. On the right sidebar, you will see a "Filter" section with all available tags
3. Click on a tag to filter products that have that tag assigned

### Frontend Display

Tags are displayed on the product detail page in the following format:

- **Heading**: "Product-Tags"
- **Tags**: Displayed as gray badges with the tag name
- **No Tags Fallback**: If a product has no tags, the text "no tags available" is displayed

## Code Implementation

### Models (products/models.py)

The `Tag` model is defined with proper type hints and docstrings:

```python
class Tag(models.Model):
    """Tag model for categorizing products with labels.

    Attributes:
        name: Unique tag name (max 100 chars)
        created_at: Timestamp when tag was created
        updated_at: Timestamp when tag was last updated
    """

    name = models.CharField(max_length=100, unique=True, help_text="Name of Tag")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Tags"

    def __str__(self) -> str:
        """Return the tag name."""
        return self.name
```

### Admin Configuration (products/admin.py)

The `TagAdmin` class provides the admin interface configuration:

```python
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for Tag model."""

    list_display = ("name", "created_at")
    search_fields = ("name",)
```

The `ProductAdmin` class includes tag filtering:

```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "average_rating", "rating_count", "created_at")
    list_select_related = ("category",)
    list_filter = ("tags",)
```

### Template Display (products/templates/product.html)

Tags are displayed on the product detail page using Django template logic:

```django
<div class="mb-3">
    <h6 class="mb-2">Product-Tags</h6>

    {% if product.tags.all %}
        <div>
            {% for tag in product.tags.all %}
                <span class="badge bg-secondary">{{ tag.name }}</span>
            {% endfor %}
        </div>
    {% else %}
        <span class="text-muted">no tags available</span>
    {% endif %}
</div>
```

## Migration

A database migration was created to implement the Tag model and the product-tag relationship. The migration file is located at:

`products/migrations/0002_tag_product_tags.py`

This migration creates the `products_tag` table and the `products_product_tags` junction table for the many-to-many relationship.

## Best Practices

1. **Keep Tag Names Consistent**: Use consistent naming conventions for tags (e.g., all lowercase or title case) to avoid duplicate tags with similar names.
2. **Regular Cleanup**: Periodically review and remove unused tags that are no longer assigned to any products.
3. **Meaningful Tags**: Use descriptive tag names that clearly indicate the product's characteristics or status.
4. **Limit Tag Count**: Avoid assigning too many tags to a single product to maintain clear organization.

## Testing

To test the Product Tags feature:

1. Access the Django admin interface at `localhost:8000/admin/`
2. Navigate to the Tags section and create a few sample tags
3. Edit a product and assign multiple tags to it
4. View the product detail page and verify that tags are displayed correctly
5. Use the tag filter in the admin Products section to verify filtering works
6. Create a product without tags and verify the "no tags available" message appears

## Future Enhancements

Possible improvements to the Product Tags feature include:

- **Tag Cloud**: Display a visual tag cloud on the products listing page
- **Frontend Filtering**: Allow users to filter products by tags from the frontend
- **Tag Descriptions**: Add descriptions to tags for better documentation
- **Tag Hierarchy**: Implement parent-child relationships between tags
- **Auto-Tagging**: Implement automated tag suggestions based on product properties
