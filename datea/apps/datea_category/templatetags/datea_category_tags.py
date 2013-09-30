from django import template
from datea_category.models import DateaCategory
from datea_category.forms import DateaFreeCategoryForm

register = template.Library()

@register.assignment_tag
def get_categories():
    return DateaCategory.tree.filter(active=True)


@register.assignment_tag
def get_free_category_form():
    return DateaFreeCategoryForm()
