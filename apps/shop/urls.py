from django.conf.urls import patterns, url
from views import *

urlpatterns = patterns('',

    # url(r'^hero-add/$', AlteregosCreateView.as_view(), name='create'),
    # url(r'^power-add/$', PowerCreateView.as_view(), name='power_create'),
    # url(r'^image-edit/(?P<pk>[\w\d]+)/$', ImageEditView.as_view(), name='image_update'),
    #
    # url(r'^(?P<pk>[\w\d]+)/$', AlteregosDetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>[\w\d]+)/edit/$', AlteregosUpdateView.as_view(), name='update'),
    # url(r'^(?P<pk>[\w\d]+)/delete/$', AlteregosDeleteView.as_view(), name='delete'),

    url(r'^add-options.html$', OptionCreate.as_view(), name='add_option'),
    url(r'^update-options/(?P<pk>[\w\d]+).html$', OptionUpdate.as_view(), name='update_option'),
    url(r'^options.html$', OptionList.as_view(), name='option_list'),

    url(r'^add-product.html$', AddProductView.as_view(), name='add_product'),
    url(r'^update-product/(?P<pk>[\w\d]+).html$', UpdateProductView.as_view(), name='update_product'),
    url(r'^(?P<category>[\w\d]+)/(?P<pk>[\w\d]+).html$', ProductDetailView.as_view(), name='product'),

    url(r'^add-category.html$', AddCategoryView.as_view(), name='add_category'),
    url(r'^(?P<category>[\w\d]+).html$', Index.as_view(), name='category'),

    url(r'^index.html$', Index.as_view(), name='index'),

)
