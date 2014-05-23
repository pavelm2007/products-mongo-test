from bson import ObjectId
from django import forms
from django.forms.formsets import formset_factory
from mongoforms import MongoForm
from mongoforms.utils import iter_valid_fields
from .models import *


class CategoryForm(forms.Form):
    category = forms.ChoiceField(required=False)
    name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        document = Category
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [('', '---------')] + [(obj.id, obj.name) for obj in Category.objects]
        if self.instance:
            self.fields['category'].initial = self.instance.category
            self.fields['name'].initial = self.instance.name
            self.fields['description'].initial = self.instance.description
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        category = self.instance if self.instance else Category()
        category_id = self.cleaned_data['category']
        category_parent = Category.objects(id=category_id).first()

        if category_parent:
            category.category = category_parent.id
        category.name = self.cleaned_data['name']
        category.description = self.cleaned_data['description']
        category.save()

        if category_parent:
            category_parent.children.append(category.id)
            category_parent.save()

        return category

    def get_action(self):
        return reverse('shop:add_category')


class ProductForm(forms.Form):
    category = forms.ChoiceField(required=False)
    name = forms.CharField()
    intro = forms.CharField(widget=forms.Textarea, required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    sku = forms.CharField(required=False)
    price = forms.DecimalField(max_digits=9, decimal_places=2)
    old_price = forms.DecimalField(max_digits=9, decimal_places=2, required=False)
    meta_keywords = forms.CharField(required=False)
    meta_description = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [('', '---------')] + [(obj.id, obj.name) for obj in Category.objects]
        if self.instance:
            self.fields['category'].initial = self.instance.category.id
            self.fields['name'].initial = self.instance.name
            self.fields['intro'].initial = self.instance.intro
            self.fields['description'].initial = self.instance.description
            self.fields['sku'].initial = self.instance.sku
            self.fields['price'].initial = self.instance.price
            self.fields['old_price'].initial = self.instance.old_price
            self.fields['meta_keywords'].initial = self.instance.meta_keywords
            self.fields['meta_description'].initial = self.instance.meta_description
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        obj = self.instance if self.instance else Product()
        category_id = self.cleaned_data['category']
        category = Category.objects(id=category_id).first()
        obj.category = category
        obj.name = self.cleaned_data['name']
        obj.intro = self.cleaned_data['intro']
        obj.description = self.cleaned_data['description']
        obj.sku = self.cleaned_data['sku']
        obj.price = self.cleaned_data['price']
        obj.old_price = self.cleaned_data['old_price']
        obj.meta_keywords = self.cleaned_data['meta_keywords']
        obj.meta_description = self.cleaned_data['meta_description']
        obj.save()
        return obj

    def get_action(self):
        if self.instance:
            return reverse('shop:update_product', args=[self.instance.id])
        return reverse('shop:add_product')


class OptionForm(MongoForm):
    class Meta:
        document = Option

    def __init__(self, *args, **kwargs):
        super(OptionForm, self).__init__(*args, **kwargs)
        self.fields['type_field'].label = 'Type field'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def get_action(self):
        print(self.initial)
        if self.initial:
            return reverse('shop:update_option', args=[self.instance.id])
        return reverse('shop:add_option')


# class VariantForm(MongoForm):
#     class Meta:
#         document = Variant
#         fields = ('name', 'value',)
#
#     name = forms.ChoiceField(label='Name')
#
#     def __init__(self, *args, **kwargs):
#         super(VariantForm, self).__init__(*args, **kwargs)
#         # self.empty_permitted = False
#         self.fields['name'].choices = [('', '---------')] + [(obj.id, obj.name) for obj in Option.objects]
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'
#
#     def save(self, commit=True):
#         variant_dict = {}
#         for field_name, field in iter_valid_fields(self._meta):
#             if self.cleaned_data.get(field_name):
#                 variant_dict.update(
#                     {
#                         field_name: self.cleaned_data.get(field_name),
#                     }
#                 )
#                 # setattr(self.instance, field_name, self.cleaned_data.get(field_name))
#         # print self.instance
#         return variant_dict
class VariantForm(forms.Form):
    name = forms.ChoiceField(label='Name', required=True)
    value = forms.CharField(label='Value', required=True)

    class Meta:
        fields = ('name', 'value')

    def __init__(self, *args, **kwargs):
        super(VariantForm, self).__init__(*args, **kwargs)
        # self.empty_permitted = False
        self.fields['name'].choices = [(None, '---------')] + [(obj.id, obj.name) for obj in Option.objects]
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


VariantFormSet = formset_factory(VariantForm)

