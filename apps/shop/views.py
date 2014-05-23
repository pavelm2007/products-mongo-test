import json

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from extra_cbv.views.formset import FormsetMixin, ProcessFormsetView
from .models import Category, Product
from .forms import *


class ShopMixin(object):
    def get_context_data(self, **kwargs):
        ctx = super(ShopMixin, self).get_context_data(**kwargs)
        category_list = Category.objects(category__exists=False)
        category_id = self.kwargs.get('category', None)
        if category_id and category_id != 'index':
            current_category = Category.objects(id=category_id).first()
            ctx['current_category'] = current_category
            if len(current_category.children) == 0:
                print self.get_options(**kwargs)
        ctx.update(
            {
                'category_list': category_list,
            }
        )
        return ctx

    def get_options(self, **kwargs):
        queryset = self.get_queryset(**kwargs)
        variant_list = []
        options_dict = {}
        if queryset:
            for item in queryset:
                variant_list.extend(item.get_list())
            for variant in variant_list:
                print variant
                for key, val in variant.items():
                    if options_dict.has_key(key):
                        list_item = options_dict[key]
                        values = list_item['values']
                        values.extend(val)
                        list_item['values'] = values
                        options_dict.update(
                            {
                                key: list_item
                            }
                        )
                    else:
                        val_list = []
                        list_item = {
                            'name': key.name,
                            'values': val_list.insert(0, val),
                        }
                        options_dict.update({key: list_item})

            print options_dict
        return


class ShopFormMixin(ShopMixin):
    def get_object(self, queryset=None):
        return self.model.objects(id=self.kwargs['pk']).first()


class Index(ShopMixin, ListView):
    model = Product
    template_name = 'shop/index.html'

    def get_queryset(self, **kwargs):
        category = self.kwargs.get('category', None)
        if category and category != 'index':
            qs = self.model.objects(category=ObjectId(category))
        else:
            qs = self.model.objects()
        return qs


class ProductDetailView(ShopMixin, DetailView):
    model = Product
    template_name = 'shop/product_detail.html'

    def get_object(self, queryset=None):
        return self.model.objects(id=self.kwargs['pk']).first()


class AddCategoryView(ShopMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'shop/form_create.html'


class AddProductView(ShopMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/form_create.html'


class UpdateProductView(ShopFormMixin, FormsetMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/form_create.html'

    formset_form = VariantForm
    # formset_class = VariantFormSet
    formset_extra = 1
    can_order = False
    can_delete = True
    max_num = None
    # initial = {}

    def get_object(self, queryset=None):
        obj = super(UpdateProductView, self).get_object(queryset=None)
        return obj

    def form_valid(self, form):
        self.object = form.save()
        formset = self.get_formset()
        options = []
        option_is_change = False
        for form_item in formset:
            if form_item.is_valid() and form_item.has_changed():
                fields = {}
                if form_item.cleaned_data.get('name'):
                    fields['name'] = form_item.cleaned_data.get('name')
                else:
                    continue
                if form_item.cleaned_data.get('value'):
                    fields['value'] = form_item.cleaned_data.get('value')
                else:
                    continue
                options.append(Variant(**fields))
        self.object.options = options
        print options
        print option_is_change
        # else:
        #     return self.form_invalid(form)
        # if formset.is_valid():
        #     options = []
        #     option_is_change = False
        #     for form_item in formset:
        #         if form_item.is_valid():
        #             fields = {}
        #             if form_item.cleaned_data.get('name'):
        #                 fields['name'] = form_item.cleaned_data.get('name')
        #             else:
        #                 continue
        #             if form_item.cleaned_data.get('value'):
        #                 fields['value'] = form_item.cleaned_data.get('value')
        #             else:
        #                 continue
        #             options.append(Variant(**fields))
        #             # for option in options:
        #             #     if option['name'] == fields['name'] and option['value'] != fields['value']:
        #             #         option['value'] = fields['value']
        #             #         option_is_change = True
        #             #
        #             # if not options:
        #             #     options.append(Variant(**fields))
        #             #     option_is_change = True
        #             # if not option_is_change:
        #             #     options.append(Variant(**fields))
        #             #     option_is_change = True
        #     self.object.options = options
        #     print options
        #     print option_is_change
        # else:
        #     return self.form_invalid(form)
        self.object.save()
        return super(UpdateProductView, self).form_valid(form)
        # return HttpResponseRedirect(reverse('shop:index'))

    def get_formset_class_kwargs(self):
        """
        Returns keywords arguments to create the formset class
        """
        return {
            'form': self.formset_form,
            'formset': self.formset_class,
            'extra': self.formset_extra,
            'can_order': self.can_order,
            'can_delete': self.can_delete,
            'max_num': self.max_num
        }

    def get_formset_initial(self):
        variant_list = self.object.options
        formset_initial = []
        for variant in variant_list:
            formset_initial.append(
                {
                    'name': variant.name,
                    'value': variant.value,
                }
            )
        return formset_initial

    def get_formset_kwargs(self):
        kwargs = FormMixin.get_form_kwargs(self)
        kwargs.update(
            {
                'initial': self.get_formset_initial(),
            }
        )
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(UpdateProductView, self).get_context_data(**kwargs)
        formset = self.get_formset()

        ctx['formset'] = formset
        return ctx


class OptionList(ShopMixin, ListView):
    model = Option
    template_name = 'shop/options/list_options.html'

    def get_queryset(self):
        return self.model.objects()


class OptionCreate(CreateView):
    model = Option
    form_class = OptionForm
    template_name = 'shop/options/create.html'
    success_url = reverse_lazy('shop:option_list')


class OptionUpdate(UpdateView):
    model = Option
    form_class = OptionForm
    template_name = 'shop/options/create.html'
    success_url = reverse_lazy('shop:option_list')

    def get_object(self, queryset=None):
        return self.model.objects(id=self.kwargs['pk']).first()
