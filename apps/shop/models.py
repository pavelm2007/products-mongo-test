# -*- coding: utf-8 -*-
import decimal

from datetime import datetime
from django.db import models
from django.core.urlresolvers import reverse

from mongoengine import *

from .helper import *

TYPE_FIELD_CHOICE = (
    ('choice', 'Choice'),
    ('multiple_checkbox', 'Multiple checkbox'),
    ('range', 'Min-Max'),
)

class Option(Document):
    name = StringField(max_length=150)
    type_field = StringField(max_length=15, choices=TYPE_FIELD_CHOICE)
    meta = {
        'collection': 'Option',
        # 'indexes': ['name'],
        #     'ordering': ['name'],
    }

    def get_update_url(self):
        return reverse('shop:update_option', args=[self.id])


#
# class GroupVariant(EmbeddedDocument):
#     name = StringField()
#     options = ListField(EmbeddedDocument(Option))


class Variant(EmbeddedDocument):
    name = ObjectIdField()
    value = StringField(max_length=15)

    def to_dict(self):
        return mongo_to_dict(self, [])


class Category(Document):
    # category = ReferenceField('self', dbref=True, required=False)

    category = StringField(required=False)
    name = StringField(max_length=255, )
    description = StringField(required=False)
    count_products = IntField(required=False)
    children = ListField(required=False)

    meta = {
        'collection': 'Category',
        'indexes': ['name'],
        'ordering': ['name'],
    }

    def get_absolute_url(self):
        return reverse('shop:category', args=[self.id])

    def get_child(self):
        return Category.objects(category=self.id)

    def get_all_children(self, include_self=True):
        r = []
        if include_self:
            r.append(self)
        for c in Category.objects(category=self.id):
            r = r + c.get_all_children()
            # r.append(c.get_all_children())
        return r


class Product(Document):
    category = ReferenceField(Category, required=False)
    name = StringField(max_length=255)
    intro = StringField(required=False)
    description = StringField(required=False)
    sku = StringField(max_length=64, required=False)
    price = DecimalField(precision=2, rounding=decimal.ROUND_HALF_EVEN)
    old_price = DecimalField(precision=2, rounding=decimal.ROUND_HALF_EVEN, required=False)

    options = ListField(EmbeddedDocumentField(Variant))

    meta_keywords = StringField(max_length=255, required=False)
    meta_description = StringField(max_length=255, required=False)
    created_at = DateTimeField(default=datetime.now())

    related_products = ListField(required=False)

    meta = {
        'collection': 'Products',
        'indexes': ['name'],
        'ordering': ['name'],
    }

    def get_absolute_url(self):
        return reverse('shop:product', args=[self.category.id, self.id])

    def get_update_url(self):
        return reverse('shop:update_product', args=[self.id])

    def get_option_list(self):
        options_list = self.options
        qs = {}
        for option in options_list:
            qs.update(
                {Option.objects(id=option.name).first(): option.value}
            )
        return qs

    def get_list(self):
        option_list = self.options
        qs = []
        for option in option_list:
            qs.append({Option.objects(id=option.name).first(): option.value})
        return qs
