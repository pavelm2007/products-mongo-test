from django import template
from ..models import Category

register = template.Library()


@register.inclusion_tag('shop/_include/category_tree.html', takes_context=True)
def category_tree(context, category):
    children = Category.objects(category=category.id)
    return {'category': category, 'children': children, }
