# from django.urls import path
from django.urls import path
from django.views.generic import TemplateView

from product.views.product import CreateProductView, product_view, search_view
from product.views.variant import VariantView, VariantCreateView, VariantEditView

app_name = "product"

urlpatterns = [

    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    path('create/', CreateProductView.as_view(), name='create.product'),
  
    path('list/', product_view, name='list.product'),
    path('searchlist/', search_view, name='search_view'),
 
]
